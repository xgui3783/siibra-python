import pandas as pd

import requests

url = "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/hbp-d000061_BB-CorticalCellDistribution_pub/Visual_FG3/v1.0/2116/0002/segments.txt"
f = pd.read_csv(url, comment="#", sep=" ", names=["x", "y", "area(micron**2)", "layer", "label"])

resp = requests.get(url, headers={
    "Range": "bytes=0-128"
})

resp.raise_for_status()

print(resp.text)

def foo(first_arg=None, *args, foo=None, **kwargs):
    pass

foo(foo="foo")