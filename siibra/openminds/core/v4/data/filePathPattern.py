# generated by datamodel-codegen:
#   filename:  https://raw.githubusercontent.com/HumanBrainProject/openMINDS/3fa86f956b407b2debf47c2e1b6314e37579c707/v3/core/v4/data/filePathPattern.schema.json

from typing import Any, Dict

from pydantic import Field
from siibra.openminds.base import SiibraBaseModel


class Model(SiibraBaseModel):
    id: str = Field(..., alias='@id', description='Metadata node identifier.')
    type: str = Field(..., alias='@type')
    grouping_type: Dict[str, Any] = Field(
        ...,
        alias='groupingType',
        title='groupingType',
    )
    regex: str = Field(
        ..., alias='regex', title='regex'
    )
