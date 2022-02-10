# generated by datamodel-codegen:
#   filename:  https://raw.githubusercontent.com/HumanBrainProject/openMINDS/3fa86f956b407b2debf47c2e1b6314e37579c707/v3/core/v4/miscellaneous/funding.schema.json

from typing import Any, Dict, Optional

from pydantic import Field
from siibra.openminds.base import SiibraBaseModel


class Model(SiibraBaseModel):
    id: str = Field(..., alias='@id', description='Metadata node identifier.')
    type: str = Field(..., alias='@type')
    acknowledgement: Optional[str] = Field(
        None,
        alias='acknowledgement',
        description='Offical declaration or avowal of appreciation of an act or achievement.',
        title='acknowledgement',
    )
    award_number: Optional[str] = Field(
        None,
        alias='awardNumber',
        description='Machine-readable identifier for a benefit that is conferred or bestowed on the basis of merit or need.',
        title='awardNumber',
    )
    award_title: Optional[str] = Field(
        None,
        alias='awardTitle',
        description='Human-readable identifier for a benefit that is conferred or bestowed on the basis of merit or need.',
        title='awardTitle',
    )
    funder: Dict[str, Any] = Field(
        ...,
        alias='funder',
        description='Legal person that provides money for a particular purpose.',
        title='funder',
    )
