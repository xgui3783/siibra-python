# Copyright 2018-2020 Institute of Neuroscience and Medicine (INM-1), Forschungszentrum Jülich GmbH

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import logger, spaces, volumesrc, parcellationmap
from .space import Space
from .region import Region
from .config import ConfigurationRegistry
from .commons import create_key,MapType,ParcellationIndex
from .dataset import Dataset
from .volumesrc import HasVolumeSrc
from typing import Union
from memoization import cached

class ParcellationVersion:
    def __init__(self, name=None, collection=None, prev_id=None, next_id=None, deprecated=False):
        self.name=name
        self.collection=collection
        self.next_id=next_id
        self.prev_id=prev_id
        self.deprecated=deprecated

    def __eq__(self,other):
        return all([
            self.name==other.name,
            self.collection==other.collection])
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return  self.name

    def __iter__(self):
        yield 'name', self.name
        yield 'prev', self.prev.id if self.prev is not None else None
        yield 'next', self.next.id if self.next is not None else None
        yield 'deprecated', self.deprecated

    def __lt__(self,other):
        """ < operator, useful for sorting by version"""
        successor = self.next
        while successor is not None:
            if successor.version==other:
                return True
            successor = successor.version.next
        return False

    @property
    def next(self):
        if self.next_id is None:
            return None
        try:
            return REGISTRY[self.next_id]
        except IndexError:
            return None
        except NameError:
            logger.warning('Accessing REGISTRY before its declaration!')
    
    @property
    def prev(self):
        if self.prev_id is None:
            return None
        try:
            return REGISTRY[self.prev_id]
        except IndexError:
            return None
        except NameError:
            logger.warning('Accessing REGISTRY before its declaration!')

    @staticmethod
    def from_json(obj):
        """
        Provides an object hook for the json library to construct a
        ParcellationVersion object from a json string.
        """
        if obj is None:
            return None
        return ParcellationVersion(
            obj.get('name', None), 
            obj.get('collectionName',None),
            prev_id=obj.get('@prev', None), 
            next_id=obj.get('@next', None),
            deprecated=obj.get('deprecated', False))

class Parcellation(Dataset,HasVolumeSrc):

    _regiontree_cached = None

    def __init__(self, identifier : str, name : str, version=None, modality=None, regiondefs=[]):
        """
        Constructs a new parcellation object.

        Parameters
        ----------
        identifier : str
            Unique identifier of the parcellation
        name : str
            Human-readable name of the parcellation
        version : str or None
            a version specification, optional
        modality  :  str or None
            a specification of the modality used for creating the parcellation.
        """
        Dataset.__init__(self,identifier,name)
        HasVolumeSrc.__init__(self)
        self.key = create_key(name)
        self.version = version
        self.publications = []
        self.description = ""
        self.modality = modality
        self._regiondefs = regiondefs

        # If set, thresholded continuous maps will be preferred
        # over static labelled maps for building and using region masks.
        # This will influence the shape of region masks used for filtering.
        self.continuous_map_threshold = None

    @property
    def regiontree(self):
        if self._regiontree_cached is None:
            self._regiontree_cached = Region(self.name,self,ParcellationIndex(None,None))
            try:
                    self._regiontree_cached.children = tuple( 
                        Region.from_json(regiondef,self) 
                        for regiondef in self._regiondefs )
            except Exception as e:
                logger.error(f"Could not generate child regions for {self.name}")
                raise(e)
        return self._regiontree_cached

    def get_volume_src(self, space: Space):
        """
        Get volumes sources for the parcellation in the requested template space.

        Parameters
        ----------
        space : Space
            template space

        Yields
        ------
        A list of volume sources
        """
        if not self.supports_space(space):
            raise ValueError('Parcellation "{}" does not provide volume sources for space "{}"'.format(
                str(self), str(space) ))
        return self.volume_src[space]

    @cached
    def get_map(self, space=None, maptype:Union[str,MapType]=MapType.LABELLED):
        """
        Get the volumetric maps for the parcellation in the requested
        template space. This might in general include multiple 
        3D volumes. For example, the Julich-Brain atlas provides two separate
        maps, one per hemisphere. Per default, multiple maps are concatenated into a 4D
        array, but you can choose to retrieve a dict of 3D volumes instead using `return_dict=True`.

        Parameters
        ----------
        space : Space or str
            template space specification 
        maptype : MapType (default: MapType.LABELLED)
            Type of map requested (e.g., continous or labelled, see commons.MapType)
            Use MapType.CONTINUOUS to request probability maps.

        Yields
        ------
        A ParcellationMap representing the volumetric map.
        """
        if isinstance(maptype,str):
            maptype = MapType[maptype.upper()]
        if space is None:
            spaceobj = next(iter(self.volume_src.keys()))
            if len(self.volume_src)>1:
                logger.warning(f'Parcellation "{str(self)}" provides maps in multiple spaces, but no space was specified.\nUsing the first, "{str(space)}"')
        else:
            spaceobj = spaces[space]

        if not self.supports_space(spaceobj):
            raise ValueError(f'Parcellation "{self.name}" does not provide a map for space "{spaceobj.name}"')

        return parcellationmap.create_map(self,spaceobj,maptype)

    @property
    def labels(self):
        return self.regiontree.labels

    @property
    def names(self):
        return self.regiontree.names

    def supports_space(self,space : Space):
        """
        Return true if this parcellation supports the given space, else False.
        """
        spaceobj = spaces[space]
        return any(vsrc.space_id==spaceobj.id for vsrc in self.volume_src)
        #return spaceobj in self.volume_src.keys()

    def decode_region(self,regionspec:Union[str,int,ParcellationIndex,Region],build_group=True):
        """
        Given a unique specification, return the corresponding region.
        The spec could be a label index, a (possibly incomplete) name, or a
        region object.
        This method is meant to definitely determine a valid region. Therefore, 
        if no match is found, it raises a ValueError. If it finds multiple
        matches, it tries to return only the common parent node. If there are
        multiple remaining parent nodes, which is rare, a custom group region is constructed.

        Parameters
        ----------
        regionspec : any of 
            - a string with a possibly inexact name, which is matched both
              against the name and the identifier key, 
            - an integer, which is interpreted as a labelindex,
            - a region object
            - a full ParcellationIndex

        Return
        ------
        Region object
        """
        candidates = self.regiontree.find(regionspec,select_uppermost=True)
        if not candidates:
            raise ValueError("Regionspec {} could not be decoded under '{}'".format(
                regionspec,self.name))
        elif len(candidates)==1:
            return candidates[0]
        else:
            if build_group:
                logger.debug(f"The specification '{regionspec}' resulted more than one region. A group region is returned.")
                return Region._build_grouptree(candidates,self)
            else:
                raise RuntimeError(f"Decoding of spec {regionspec} resulted in multiple matches: {','.join(r.name for r in candidates)}.")


    @cached
    def find_regions(self,regionspec):
        """
        Find regions with the given specification in this parcellation.

        Parameters
        ----------
        regionspec : any of 
            - a string with a possibly inexact name, which is matched both
              against the name and the identifier key, 
            - an integer, which is interpreted as a labelindex
            - a region object

        Yield
        -----
        list of matching regions
        """
        return self.regiontree.find(regionspec)

    def __str__(self):
        return self.name

    def __repr__(self):
        return  self.name

    def __eq__(self,other):
        """
        Compare this parcellation with other objects. If other is a string,
        compare to key, name or id.
        """
        if isinstance(other,Parcellation):
            return self.id==other.id
        elif isinstance(other,str):
            return any([
                self.name==other, 
                self.key==other,
                self.id==other])
        else:
            raise ValueError("Cannot compare object of type {} to Parcellation".format(type(other)))

    def __iter__(self):
        """
        Returns an iterator that goes through all regions in this parcellation
        """
        return self.regiontree.__iter__()

    def __getitem__(self,regionspec:Union[str,int]):
        """
        Retrieve a region object from the parcellation by labelindex or partial name.
        """
        return self.decode_region(regionspec)

    @staticmethod
    def from_json(obj):
        """
        Provides an object hook for the json library to construct a Parcellation
        object from a json string.
        """
        required_keys = ['@id','name','shortName','volumeSrc','regions']
        if any([k not in obj for k in required_keys]):
            return obj

        # create the parcellation, it will create a parent region node for the regiontree.
        result = Parcellation(obj['@id'], obj['shortName'], regiondefs=obj['regions'])
        
        for spec in obj.get('volumeSrc',[]):
            result._add_volumeSrc(spec)

        for spec in obj.get('originDataset',[]):
            result._add_originDatainfo(spec)
        
        if '@version' in obj:
            result.version = ParcellationVersion.from_json(obj['@version'])

        if 'modality' in obj:
            result.modality = obj['modality']

        if 'description' in obj:
            result.description = obj['description']

        if 'publications' in obj:
            result.publications = obj['publications']

        return result

REGISTRY = ConfigurationRegistry('parcellations', Parcellation)
