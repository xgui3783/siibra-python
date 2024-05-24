import json
from typing import TypedDict, List, Any
import calendar

from .base import register_content_type
from ...cache import fn_call_cache


# inline doc generated by pasting json to
# https://json2pyi.pages.dev/#TypedDictInline

PublishedPrintOrPublishedOrIssued = TypedDict(
    "PublishedPrintOrPublishedOrIssued", {"date-parts": List[List[int]]}
)

JournalIssue = TypedDict(
    "JournalIssue", {"issue": str, "published-print": PublishedPrintOrPublishedOrIssued}
)

Primary = TypedDict("Primary", {"URL": str})

Resource = TypedDict("Resource", {"primary": Primary})

CreatedOrDepositedOrIndexed = TypedDict(
    "CreatedOrDepositedOrIndexed",
    {"date-parts": List[List[int]], "date-time": str, "timestamp": int},
)

Link = TypedDict(
    "Link",
    {
        "URL": str,
        "content-type": str,
        "content-version": str,
        "intended-application": str,
    },
)

Author = TypedDict(
    "Author", {"given": str, "family": str, "sequence": str, "affiliation": List[Any]}
)

ContentDomain = TypedDict(
    "ContentDomain", {"domain": List[Any], "crossmark-restriction": bool}
)

ReturnedResult = TypedDict(
    "ReturnedResult",
    {
        "indexed": CreatedOrDepositedOrIndexed,
        "reference-count": int,
        "publisher": str,
        "issue": str,
        "content-domain": ContentDomain,
        "published-print": PublishedPrintOrPublishedOrIssued,
        "DOI": str,
        "type": str,
        "created": CreatedOrDepositedOrIndexed,
        "page": str,
        "source": str,
        "is-referenced-by-count": int,
        "title": str,
        "prefix": str,
        "volume": str,
        "author": List[Author],
        "member": str,
        "container-title": str,
        "original-title": List[Any],
        "language": str,
        "link": List[Link],
        "deposited": CreatedOrDepositedOrIndexed,
        "score": int,
        "resource": Resource,
        "subtitle": List[Any],
        "short-title": List[Any],
        "issued": PublishedPrintOrPublishedOrIssued,
        "references-count": int,
        "journal-issue": JournalIssue,
        "alternative-id": List[str],
        "URL": str,
        "relation": Any,
        "ISSN": List[str],
        "subject": List[Any],
        "container-title-short": str,
        "published": PublishedPrintOrPublishedOrIssued,
    },
)


CITE_PROC_JSON = "application/vnd.citationstyles.csl+json"


def stringify_author(author: Author):
    return f"{author['family']} {author['given']}"


# doc at https://github.com/citation-style-language/schema#csl-json-schema


@fn_call_cache
@register_content_type(CITE_PROC_JSON)
def process_cite_proc_json(bytes: bytes) -> str:
    result: ReturnedResult = json.loads(bytes)

    authors = result["author"]
    title = result[
        "title"
    ]  # Structural Brain Magnetic Resonance Imaging of Limbic and Thalamic Volumes in Pediatric Bipolar Disorder
    journal_title = result["container-title"]  # American Journal of Psychiatry
    journal_issue = result.get("issue")  # 7
    journal_volume = result.get(
        "volume"
    )  # https://dx.doi.org/10.1016/B978-012693019-1/50023-X has no volume
    published = result["published"]["date-parts"]
    page = result["page"]

    assert len(published) == 1
    published_str = ""
    try:
        published_str += str(published[0][0])
        published_str += calendar.month_name[int(published[0][1])]
    except IndexError:
        pass

    journal_str = ""
    if journal_volume:
        journal_str += journal_volume
    if journal_issue:
        journal_str += f" ({journal_issue})"
    rest_str = f"{published_str};{journal_str}:{page}"

    "Frazier JA, Chiu S, Breeze JL, Makris N, Lange N, Kennedy DN, Herbert MR, Bent EK, Koneru VK, Dieterich ME, Hodge SM, Rauch SL, Grant PE, Cohen BM, Seidman LJ, Caviness VS, Biederman J."
    "Structural brain magnetic resonance imaging of limbic and thalamic volumes in pediatric bipolar disorder."
    "Am J Psychiatry."
    "2005 Jul;162(7):1256-65"
    first = [
        stringify_author(author) for author in authors if author["sequence"] == "first"
    ]
    other = [
        stringify_author(author) for author in authors if author["sequence"] != "first"
    ]
    authors_str = ", ".join([*first, *other])

    return f"{authors_str}. {title}. {journal_title}. {rest_str}"
