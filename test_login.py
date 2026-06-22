from divoom_api import DivoomGalleryAPI

api = DivoomGalleryAPI()
# We don't have valid credentials, but we can verify the method signature and request format works without crashing
api.login("test@test.com", "password")
