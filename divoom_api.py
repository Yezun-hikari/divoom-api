import urllib.request
import json
import ssl

class DivoomGalleryAPI:
    """
    A Python wrapper for the Divoom Gallery API.
    Allows searching for pixel art without requiring an account.
    """

    BASE_URL = "https://app.divoom-gz.com"
    FILE_URL = "https://f.divoom-gz.com/"

    # Size mapping based on API observations
    # 1: 16x16, 2: 32x32, 4: 64x64, 16: 128x128
    SIZE_MAP = {
        16: 1,
        32: 2,
        64: 4,
        128: 16
    }

    def __init__(self):
        # Setting up a permissive SSL context if needed
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def _post(self, endpoint, data):
        url = f"{self.BASE_URL}/{endpoint}"
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req, context=self.ctx) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
                else:
                    raise Exception(f"HTTP Error: {response.status}")
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def search_gallery(self, keyword, size=64, return_cnt=20, base_cnt=0):
        """
        Searches the Divoom gallery for a specific keyword and size.

        :param keyword: The search term (e.g., 'mario', 'pokemon')
        :param size: The dimension of the pixel art (16, 32, 64, or 128). Defaults to 64.
        :param return_cnt: Number of results to return per page. Defaults to 20.
        :param base_cnt: Offset for pagination. Defaults to 0.
        :return: A list of dictionaries containing image metadata and download URLs.
        """
        if size not in self.SIZE_MAP:
            raise ValueError(f"Invalid size '{size}'. Allowed sizes are: {list(self.SIZE_MAP.keys())}")

        file_size_id = self.SIZE_MAP[size]

        data = {
            "KeyWord": keyword,
            "ReturnCnt": return_cnt,
            "BaseCnt": base_cnt,
            "FileSize": file_size_id
        }

        response = self._post("SearchGalleryV2", data)

        results = []
        if response and response.get("ReturnCode") == 0:
            file_list = response.get("FileList", [])
            for item in file_list:
                # Add full download URL for convenience
                file_id = item.get("FileId")
                if file_id:
                    item["DownloadUrl"] = f"{self.FILE_URL}{file_id}"
                results.append(item)

        return results

    def get_hot_files(self, size=64, return_cnt=20, base_cnt=0):
        """
        Gets trending (hot) files. Note: For 64x64, the "Hot/GetHotFiles32" or equivalent
        sometimes lists various sizes or you might want to fetch trending artists.
        """
        if size == 32:
            endpoint = "Hot/GetHotFiles32"
        else:
            print("Note: Official trending endpoint without token seems limited. 'Hot/GetHotFiles32' is available for 32x32. Returning that if you want.")
            endpoint = "Hot/GetHotFiles32"

        data = {
            "ReturnCnt": return_cnt,
            "BaseCnt": base_cnt
        }

        response = self._post(endpoint, data)

        results = []
        if response and response.get("ReturnCode") == 0:
            vendors = response.get("VendorList", [])
            for vendor in vendors:
                file_list = vendor.get("FileList", [])
                for item in file_list:
                    file_id = item.get("FileId")
                    if file_id:
                        item["DownloadUrl"] = f"{self.FILE_URL}{file_id}"
                    results.append(item)

        return results

    def get_hot_experts(self, return_cnt=10, base_cnt=0):
        """
        Fetches trending artists on Divoom.
        """
        data = {
            "ReturnCnt": return_cnt,
            "BaseCnt": base_cnt
        }
        response = self._post("Cloud/GetHotExpert", data)

        if response and response.get("ReturnCode") == 0:
            return response.get("ExpertList", [])
        return []

if __name__ == "__main__":
    api = DivoomGalleryAPI()

    print("\n--- Search Results ---")
    results = api.search_gallery("mario", size=64, return_cnt=1)
    print(json.dumps(results, indent=2))

    print("\n--- Hot Experts ---")
    experts = api.get_hot_experts(return_cnt=1)
    print(json.dumps(experts, indent=2))
