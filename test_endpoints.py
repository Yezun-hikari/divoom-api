import urllib.request
import json
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://appin.divoom-gz.com/SearchGalleryV2"
data = {"KeyWord": "minecraft", "ReturnCnt": 10, "BaseCnt": 0, "FileSize": 4}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        print("SearchGalleryV2 on appin:", json.loads(response.read().decode('utf-8')))
except Exception as e:
    print(e)

url = "https://app.divoom-gz.com/SearchGalleryV2"
req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        print("SearchGalleryV2 on app:", json.loads(response.read().decode('utf-8')))
except Exception as e:
    print(e)
