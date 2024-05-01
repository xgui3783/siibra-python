
from siibra import get_region
from siibra.locations import BoundingBox
from siibra.features_beta import get, modality
from siibra.features_beta.attributes.meta_attributes import ModalityAttribute

# reg = get_region("julich brain 2.9", "hoc1")
# features = get(reg, "receptor fingerprint")
# f = features[0]
# data = list(f.get_data())[0]
# data = [datum for f in features for datum in f.get_data()]
# assert len(data) > 0, f"expected at least 1 data"

# bbox = BoundingBox(
#     (-11, -11, -11),
#     (11, 11, 11),
#     "big brain"
# )
# features = get(bbox, "cell body staining")


# print(
#     modality.__dir__()
# )
features = get(None, modality.SEGMENTED_CELL_BODY_DENSITY)
feat = features[0]
attrs = feat.attributes