import pytest
from unittest.mock import patch, Mock

from dataclasses import replace
from typing import Type
from itertools import chain, product


from siibra.attributes import locations
from siibra.attributes.locations import Point, BoundingBox, Location
from siibra.exceptions import InvalidAttrCompException, UnregisteredAttrCompException
from siibra.assignment.attribute_qualification import qualify, Qualification


def bbox_x_flat(dim: int):
    point0 = Point(space_id="foo", coordinate=[0, 0, 0])
    point1 = Point(space_id="foo", coordinate=[100, 100, 100])
    coords1 = list(point1.coordinate)
    coords1[dim] = 1
    point1 = replace(point1, coordinate=coords1)

    delta = Point(space_id="foo", coordinate=[5 if v == dim else 0 for v in range(3)])

    p00 = replace(point0)
    p01 = replace(point1)

    p10 = replace(point0)
    p10 += delta
    p11 = replace(point1)
    p11 += delta

    p20 = replace(point0)
    p20 += delta
    p21 = replace(point1)
    p21 += delta

    return [
        BoundingBox(
            space_id="foo",
            minpoint=list(minpoint.coordinate),
            maxpoint=list(maxpoint.coordinate),
        )
        for minpoint, maxpoint in (
            (p00, p01),
            (p10, p11),
            (p20, p21),
        )
    ]


flatxbbox, flatybbox, flatzbbox = [bbox_x_flat(dim) for dim in range(3)]


@patch.object(Location, "warp")
def test_qualify_different_space(warp_mock: Mock):
    warp_mock.side_effect = RuntimeError
    bboxfoo = BoundingBox(space_id="foo", minpoint=[0, 0, 0], maxpoint=[1, 1, 1])
    bboxbar = BoundingBox(
        space_id="bar",
        minpoint=[0, 0, 0],
        maxpoint=[1, 1, 1],
    )
    with pytest.raises(UnregisteredAttrCompException):
        qualify(bboxfoo, bboxbar)
    warp_mock.assert_called_once_with(bboxbar.space_id)


@pytest.mark.parametrize(
    "bbox1, bbox2",
    chain(
        product(flatxbbox, flatybbox),
        product(flatybbox, flatxbbox),
        product(flatxbbox, flatzbbox),
        product(flatybbox, flatzbbox),
    ),
)
def test_qualify_bbox_overlaps(bbox1: BoundingBox, bbox2: BoundingBox):
    assert qualify(bbox1, bbox2) == Qualification.OVERLAPS


@pytest.mark.parametrize(
    "bbox1, bbox2",
    chain(
        product(flatxbbox, flatxbbox),
        product(flatybbox, flatybbox),
        product(flatzbbox, flatzbbox),
    ),
)
def test_qualify_no_overlap(bbox1: BoundingBox, bbox2: BoundingBox):
    if bbox1 == bbox2:
        return
    assert qualify(bbox1, bbox2) is None


bbox_foo_5_10 = BoundingBox(space_id="foo", minpoint=[5, 5, 5], maxpoint=[10, 10, 10])


@pytest.mark.parametrize(
    "arg1, arg2, expected, ExCls",
    [
        [bbox_foo_5_10, Point(coordinate=[0, 0, 0], space_id="foo"), None, None],
        [bbox_foo_5_10, Point(coordinate=[7, 0, 7], space_id="foo"), None, None],
        [bbox_foo_5_10, Point(coordinate=[7, 15, 7], space_id="foo"), None, None],
        [
            bbox_foo_5_10,
            Point(coordinate=[7, 7, 7], space_id="bar"),
            None,
            UnregisteredAttrCompException,
        ],
        [
            Point(coordinate=[7, 7, 7], space_id="foo"),
            bbox_foo_5_10,
            Qualification.CONTAINED,
            None,
        ],
        [
            bbox_foo_5_10,
            Point(coordinate=[7, 7, 7], space_id="foo"),
            Qualification.CONTAINS,
            None,
        ],
        [
            bbox_foo_5_10,
            Point(coordinate=[5, 5, 5], space_id="foo"),
            Qualification.CONTAINS,
            None,
        ],
        [
            bbox_foo_5_10,
            Point(coordinate=[10, 10, 10], space_id="foo"),
            Qualification.CONTAINS,
            None,
        ],
        [
            bbox_foo_5_10,
            Point(coordinate=[10, 5, 10], space_id="foo"),
            Qualification.CONTAINS,
            None,
        ],
        [
            bbox_foo_5_10,
            Point(coordinate=[10, 7, 10], space_id="foo"),
            Qualification.CONTAINS,
            None,
        ],
    ],
)
@patch.object(Location, "warp")
def test_compare_loc_to_loc(
    warp_mock: Mock, arg1, arg2, expected: bool, ExCls: Type[Exception]
):
    warp_mock.side_effect = RuntimeError
    if ExCls:
        with pytest.raises(ExCls):
            qualify(arg1, arg2)
        return
    assert expected == qualify(arg1, arg2)
