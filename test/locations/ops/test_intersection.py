import pytest
from typing import Type
from dataclasses import replace

from siibra.locations.ops.intersection import (
    pt_pt,
    pt_ptcld,
    pt_bbox,
    ptcld_ptcld,
    ptcld_bbox,
    bbox_bbox,
    intersect,
)
from siibra.locations import Pt, PointCloud, BBox
from siibra.exceptions import InvalidAttrCompException

pt_ = Pt(space_id="bar", coordinate=[0, 0, 0])
pt0 = Pt(space_id="foo", coordinate=[0, 0, 0])
pt0b = Pt(space_id="foo", coordinate=[0, 0, 0])
pt1 = Pt(space_id="foo", coordinate=[1, 1, 1])
pt2 = Pt(space_id="foo", coordinate=[2, 2, 2])

pt_pt_args = [
    [pt0, pt0b, replace(pt0), None],
    [pt0, pt1, None, None],
    [pt0, pt_, None, InvalidAttrCompException],
]

@pytest.mark.parametrize("pta,ptb,expected,error", pt_pt_args)
def test_pt_pt(pta:Pt, ptb:Pt, expected, error: Type[Exception]):
    if error:
        with pytest.raises(error):
            pt_pt(pta, ptb)
        return
    assert expected == pt_pt(pta, ptb)

ptcld_ = PointCloud(space_id="bar",coordinates=[[0, 0, 0], [2, 2, 2]])
ptcld0 = PointCloud(space_id="foo",coordinates=[[0, 0, 0], [2, 2, 2]])
ptcld1 = PointCloud(space_id="foo",coordinates=[[1, 1, 1], [2, 2, 2]])
ptcld2 = PointCloud(space_id="foo",coordinates=[[0, 0, 0], [1, 1, 1]])
ptcld3 = PointCloud(space_id="foo",coordinates=[[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]])
ptcld4 = PointCloud(space_id="foo",coordinates=[[1, 1, 1], [2, 2, 2], [5, 5, 5], [6, 6, 6]])
ptcld5 = PointCloud(space_id="foo",coordinates=[[5, 5, 5], [6, 6, 6]])

pt_ptcld_args = [
    [pt0, ptcld0, replace(pt0), None],
    [pt0, ptcld1, None, None],
    [pt0, ptcld_, None, InvalidAttrCompException],
]

@pytest.mark.parametrize("pt, ptcld, expected, error", pt_ptcld_args)
def test_pt_ptcld(pt:Pt, ptcld:PointCloud, expected, error: Type[Exception]):
    if error:
        with pytest.raises(error):
            pt_ptcld(pt, ptcld)
        return
    assert pt_ptcld(pt, ptcld) == expected

bbox_ = BBox(space_id="bar", minpoint=[0, 0, 0], maxpoint=[2, 2, 2])
bbox0 = BBox(space_id="foo", minpoint=[0, 0, 0], maxpoint=[2, 2, 2])
bbox1 = BBox(space_id="foo", minpoint=[1, 1, 1], maxpoint=[2, 2, 2])
bbox2 = BBox(space_id="foo", minpoint=[4, 4, 4], maxpoint=[6, 6, 6])

pt_bbox_args = [
    [pt0, bbox0, replace(pt0), None],
    [pt0, bbox1, None, None],
    [pt0, bbox_, None, InvalidAttrCompException],
]

@pytest.mark.parametrize("pt, bbox, expected, error", pt_bbox_args)
def test_pt_bbox(pt: Pt, bbox: BBox, expected, error: Type[Exception]):
    if error:
        with pytest.raises(error):
            pt_bbox(pt, bbox)
        return
    assert pt_bbox(pt, bbox) == expected

ptcld_ptcld_args = [
    [ptcld0, ptcld2, replace(pt0), None],
    [ptcld0, ptcld1, Pt(space_id="foo", coordinate=[2, 2, 2]), None],
    [ptcld0, ptcld_, None, InvalidAttrCompException],
    [ptcld3, ptcld4, replace(ptcld1), None],
    [ptcld2, ptcld5, None, None],
]

@pytest.mark.parametrize("ptclda, ptcldb, expected, error", ptcld_ptcld_args)
def test_ptcld_ptcld(ptclda, ptcldb, expected, error):
    if error:
        with pytest.raises(error):
            ptcld_ptcld(ptclda, ptcldb)
        return
    assert ptcld_ptcld(ptclda, ptcldb) == expected

ptcld_bbox_args = [
    [ptcld0, bbox1, replace(pt2), None],
    [ptcld0, bbox0, replace(ptcld0), None],
    [ptcld1, bbox0, replace(ptcld1), None],
    [ptcld3, bbox0, replace(ptcld1), None],
    [ptcld5, bbox0, None, None],
    [ptcld3, bbox_, None, InvalidAttrCompException],
]

@pytest.mark.parametrize("ptcld, bbox, expected, error", ptcld_bbox_args)
def test_ptcld_bbox(ptcld, bbox, expected, error):
    if error:
        with pytest.raises(error):
            ptcld_bbox(ptcld, bbox)
        return
    assert ptcld_bbox(ptcld, bbox) == expected

bbox_bbox_args = [
    [bbox0, bbox_, None, InvalidAttrCompException],
    [bbox0, bbox1, replace(bbox1), None],
    [bbox0, bbox2, None, None],
]

@pytest.mark.parametrize("bboxa, bboxb, expected, error", bbox_bbox_args)
def test_bbox_bbox(bboxa, bboxb, expected, error):
    if error:
        with pytest.raises(error):
            bbox_bbox(bboxa, bboxb)
        return
    assert bbox_bbox(bboxa, bboxb) == expected

@pytest.mark.parametrize("loca, locb, expected, error", [
    *pt_pt_args,
    *pt_ptcld_args,
    *pt_bbox_args,
    *ptcld_ptcld_args,
    *ptcld_bbox_args,
    *bbox_bbox_args
])
def test_intersect(loca, locb, expected, error):
    if error:
        with pytest.raises(error):
            intersect(loca, locb)
        return
    assert intersect(loca, locb) == expected
