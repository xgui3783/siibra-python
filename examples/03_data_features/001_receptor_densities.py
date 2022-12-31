# Copyright 2018-2021
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

"""
Neurotransmitter receptor densities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

EBRAINS provides transmitter receptor density measurments linked to a selection of cytoarchitectonic brain regions in the human brain (Palomero-Gallagher, Amunts, Zilles et al.). These can be accessed by calling the ``siibra.get_features()`` method with the ``siibra.modalities.ReceptorDistribution`` modality, and by specifying a cytoarchitectonic region. Receptor densities come as a structured datatype which includes a regional fingerprint with average densities for different transmitters, as well as often an additional cortical density profile and a sample autoradiograph patch. They bring their own `plot()` method to produce a quick illustration.
"""


# %%
import siibra

# %%
# If we query this modality for the whole atlas instead of a particular
# brain region, all linked receptor density features
# will be returned.
parcellation = siibra.parcellations.get('julich 2.9')
all_features = siibra.get_features(parcellation, siibra.modalities.ReceptorDensityFingerprint)
print("Receptor density fingerprints found at the following anatomical anchorings:")
print("\n".join(str(f.anchor) for f in all_features))

# %%
# When providing a particular region instead, the returned list is filtered accordingly. 
# So we can directly retrieve densities for the primary visual cortex:
v1_fingerprints = siibra.get_features(
    siibra.get_region('julich 2.9', 'v1'),
    siibra.modalities.ReceptorDensityFingerprint
)
for fp in v1_fingerprints:
    fig = fp.plot()

# %%
# Each feature includes a data structure for the fingerprint, with mean and
# standard values for different receptors. The following table thus gives
# us the same values as shown in the polar plot above:
v1_fingerprints[0].data

# %%
# Many of the receptor features also provide a profile of density measurements
# at different cortical depths, resolving the change of
# distribution from the white matter towards the pial surface.
# The profile is stored as a dictionary of density measures from 0 to 100%
# cortical depth.
v1_profiles = siibra.get_features(
    siibra.get_region('julich 2.9', 'v1'),
    siibra.modalities.ReceptorDensityProfile
)
for p in v1_profiles:
    print(p.receptor)
    if "GABAA" in p.receptor:
        print(p.receptor)
        break
p.plot()
p.data

# %%
