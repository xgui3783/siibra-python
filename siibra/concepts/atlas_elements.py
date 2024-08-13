# Copyright 2018-2024
# Institute of Neuroscience and Medicine (INM-1), Forschungszentrum Jülich GmbH

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..attributes.attribute_collection import AttributeCollection
from ..attributes.descriptions import Name, SpeciesSpec, ID as _ID

MUSTHAVE_ATTRIBUTES = {Name, _ID, SpeciesSpec}


class AtlasElement(AttributeCollection):
    schema: str = "siibra/atlas_element/v0.1"

    def __post_init__(self):
        attr_types = set(map(type, self.attributes))
        assert all(
            musthave in attr_types for musthave in MUSTHAVE_ATTRIBUTES
        ), f"An AtlasElement must have {[attr_type.__name__ for attr_type in MUSTHAVE_ATTRIBUTES]} attributes."

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.ID == other.ID

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"

    def __hash__(self):
        return hash(self.ID)

    @property
    def name(self):
        return self._get(Name).value

    @property
    def ID(self):
        return self._get(_ID).value

    @property
    def species(self):
        return self._get(SpeciesSpec).value
