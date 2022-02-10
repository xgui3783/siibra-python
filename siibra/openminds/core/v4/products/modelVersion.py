# generated by datamodel-codegen:
#   filename:  https://raw.githubusercontent.com/HumanBrainProject/openMINDS/3fa86f956b407b2debf47c2e1b6314e37579c707/v3/core/v4/products/modelVersion.schema.json

from datetime import date
from typing import Any, Dict, List, Optional

from pydantic import Field, constr
from siibra.openminds.base import SiibraBaseModel


class Copyright(SiibraBaseModel):
    holder: List = Field(
        ...,
        description='Legal person in possession of something.',
        min_items=1,
        title='holder',
    )
    year: constr(regex=r'([0-9]{4})') = Field(
        ...,
        description='Cycle in the Gregorian calendar specified by a number and comprised of 365 or 366 days divided into 12 months beginning with January and ending with December.',
        title='year',
    )


class OtherContribution(SiibraBaseModel):
    contribution_type: List = Field(
        ...,
        alias='contributionType',
        description='Distinct class of what was given or supplied as a part or share.',
        min_items=1,
        title='contributionType',
    )
    contributor: Any = Field(
        ...,
        description='Legal person that gave or supplied something as a part or share.',
        title='contributor',
    )


class Model(SiibraBaseModel):
    id: str = Field(..., alias='@id', description='Metadata node identifier.')
    type: str = Field(..., alias='@type')
    accessibility: Dict[str, Any] = Field(
        ...,
        alias='accessibility',
        description='Level to which something is accessible to someone or something.',
        title='accessibility',
    )
    copyright: Optional['Copyright'] = Field(
        None,
        alias='copyright',
        description='Structured information on the copyright.',
    )
    custodian: Optional[List[Any]] = Field(
        None,
        alias='custodian',
        description="The 'custodian' is a legal person who is responsible for the content and quality of the data, metadata, and/or code of a research product.",
        min_items=1,
        title='custodian',
    )
    description: Optional[constr(max_length=2000)] = Field(
        None,
        alias='description',
        description='Longer statement or account giving the characteristics of someone or something.',
        title='description',
    )
    developer: Optional[List[Any]] = Field(
        None,
        alias='developer',
        description='Legal person that creates or improves products or services (e.g., software, applications, etc.).',
        min_items=1,
        title='developer',
    )
    digital_identifier: Optional[Dict[str, Any]] = Field(
        None,
        alias='digitalIdentifier',
        description='Digital handle to identify objects or legal persons.',
        title='digitalIdentifier',
    )
    format: Dict[str, Any] = Field(
        ...,
        alias='format',
        description='Method of digitally organizing and structuring data or information.',
        title='format',
    )
    full_documentation: Dict[str, Any] = Field(
        ...,
        alias='fullDocumentation',
        description='Non-abridged instructions, comments, and information for using a particular product.',
        title='fullDocumentation',
    )
    full_name: Optional[str] = Field(
        None,
        alias='fullName',
        description='Whole, non-abbreviated name of something or somebody.',
        title='fullName',
    )
    funding: Optional[List[Any]] = Field(
        None,
        alias='funding',
        description='Money provided by a legal person for a particular purpose.',
        min_items=1,
        title='funding',
    )
    homepage: Optional[Dict[str, Any]] = Field(
        None,
        alias='homepage',
        description='Main website of something or someone.',
        title='homepage',
    )
    how_to_cite: Optional[str] = Field(
        None,
        alias='howToCite',
        description='Preferred format for citing a particular object or legal person.',
        title='howToCite',
    )
    input_data: Optional[List[Any]] = Field(
        None,
        alias='inputData',
        description='Data that is put into a process or machine.',
        min_items=1,
        title='inputData',
    )
    is_alternative_version_of: Optional[List[Any]] = Field(
        None,
        alias='isAlternativeVersionOf',
        description='Reference to an original form where the essence was preserved, but presented in an alternative form.',
        min_items=1,
        title='isAlternativeVersionOf',
    )
    is_new_version_of: Optional[Dict[str, Any]] = Field(
        None,
        alias='isNewVersionOf',
        description='Reference to a previous (potentially outdated) particular form of something.',
        title='isNewVersionOf',
    )
    keyword: Optional[List[Any]] = Field(
        None,
        alias='keyword',
        description='Significant word or concept that are representative of something or someone.',
        max_items=5,
        min_items=1,
        title='keyword',
    )
    license: List[Any] = Field(
        ...,
        alias='license',
        description='Grant by a party to another party as an element of an agreement between those parties that permits to do, use, or own something.',
        min_items=1,
        title='license',
    )
    other_contribution: Optional['OtherContribution'] = Field(
        None,
        alias='otherContribution',
        description='Structured information on the contribution made to a research product.',
    )
    output_data: Optional[List[Any]] = Field(
        None,
        alias='outputData',
        description='Data that comes out of, is delivered or produced by a process or machine.',
        min_items=1,
        title='outputData',
    )
    related_publication: Optional[List[Any]] = Field(
        None,
        alias='relatedPublication',
        description='Reference to something that was made available for the general public to see or buy.',
        min_items=1,
        title='relatedPublication',
    )
    release_date: date = Field(
        ...,
        alias='releaseDate',
        description='Fixed date on which a product is due to become or was made available for the general public to see or buy',
        title='releaseDate',
    )
    repository: Optional[Dict[str, Any]] = Field(
        None,
        alias='repository',
        description='Place, room, or container where something is deposited or stored.',
        title='repository',
    )
    short_name: constr(max_length=30) = Field(
        ...,
        alias='shortName',
        description='Shortened or fully abbreviated name of something or somebody.',
        title='shortName',
    )
    support_channel: Optional[List[str]] = Field(
        None,
        alias='supportChannel',
        description='Way of communication used to interact with users or customers.',
        min_items=1,
        title='supportChannel',
    )
    version_identifier: str = Field(
        ...,
        alias='versionIdentifier',
        description='Term or code used to identify the version of something.',
        title='versionIdentifier',
    )
    version_innovation: str = Field(
        ...,
        alias='versionInnovation',
        description='Documentation on what changed in comparison to a previously published form of something.',
        title='versionInnovation',
    )
