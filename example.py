from divoom_api import DivoomGalleryAPI
import json

def main():
    print("Initializing Divoom Gallery API...")
    api = DivoomGalleryAPI()

    # ---------------------------------------------
    # OPTIONAL: Enter your credentials to unlock full search
    # email = "your_email@example.com"
    # password = "your_password"
    # success = api.login(email, password)
    # print(f"Login success: {success}")
    # ---------------------------------------------

    # Search Example
    print("\n--- Search Example ---")
    keyword = "Minecraft"
    size = 64
    print(f"Searching for '{keyword}' with size {size}x{size}...")
    try:
        # Note: If no results are found, it's highly likely you need to uncomment the login section above.
        results = api.search_gallery(keyword, size=size, return_cnt=3)
        if results:
            print(f"Found {len(results)} results for '{keyword}'.")
            print("First result:")
            print(json.dumps(results[0], indent=2))
        else:
            print(f"No results found for '{keyword}' at size {size}x{size}.")
            print("Please provide valid login credentials using api.login() to unlock full search capabilities.")
    except Exception as e:
        print(f"Search failed: {e}")

    # Hot Files Example
    print("\n--- Trending Files Example ---")
    print("Fetching hot trending files (32x32)...")
    try:
        hot_files = api.get_hot_files(size=32, return_cnt=3)
        if hot_files:
            print(f"Found {len(hot_files)} hot files.")
            print("First hot file:")
            print(json.dumps(hot_files[0], indent=2))
        else:
            print("No hot files returned.")
    except Exception as e:
        print(f"Failed to fetch hot files: {e}")

    # Hot Experts Example
    print("\n--- Trending Artists (Experts) Example ---")
    try:
        experts = api.get_hot_experts(return_cnt=3)
        if experts:
            print(f"Found {len(experts)} experts.")
            print("First expert:")
            print(json.dumps(experts[0], indent=2))
        else:
            print("No experts returned.")
    except Exception as e:
        print(f"Failed to fetch experts: {e}")

if __name__ == "__main__":
    main()
