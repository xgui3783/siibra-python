# generated by datamodel-codegen:
#   filename:  https://raw.githubusercontent.com/HumanBrainProject/openMINDS/3fa86f956b407b2debf47c2e1b6314e37579c707/v3/core/v4/miscellaneous/RRID.schema.json

from pydantic import Field, constr
from siibra.openminds.base import SiibraBaseModel


class Model(SiibraBaseModel):
    id: str = Field(..., alias='@id', description='Metadata node identifier.')
    type: str = Field(..., alias='@type')
    identifier: constr(
        regex=r'https://scicrunch.org/resolver/RRID:([A-Za-z]+)[_:]([A-Za-z0-9_:-]+)'
    ) = Field(
        ...,
        alias='identifier',
        description='Term or code used to identify something or someone.',
        title='identifier',
    )
