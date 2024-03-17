import requests


cookie = None
crumb = None
def get_yahoo_cookie():
        #cookie = None

        user_agent_key = "User-Agent"
        user_agent_value = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

        headers = {user_agent_key: user_agent_value}
        response = requests.get(
            "https://www.nellisauction.com/", headers=headers, allow_redirects=True
        )

        if not response.cookies:
            raise Exception("Failed to obtain Yahoo auth cookie.")

        cookie = list(response.cookies)[0]

        return cookie
    
def call_api(url, params=None):
    try:
        response = requests.get(url, params=params)

        # Check if the request was successful (status code 200)
        print(response)
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None

if __name__ == "__main__":
    # Example API endpoint (replace with your own)
    
    api_url = "https://www.nellisauction.com/search?query=bose&_data=routes/search"
    user_agent_key = "User-Agent"
    user_agent_value = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    headers = {user_agent_key: user_agent_value
               ,'Cookie': '_gac_UA-39323446-2=1.1707934689.Cj0KCQiA5rGuBhCnARIsAN11vgTjbennh2eLIf3GuQUvUfNsvFmI94tQBZcLNBeXjvY7cLeIze-ikIQaAsK8EALw_wcB; _gcl_aw=GCL.1707934689.Cj0KCQiA5rGuBhCnARIsAN11vgTjbennh2eLIf3GuQUvUfNsvFmI94tQBZcLNBeXjvY7cLeIze-ikIQaAsK8EALw_wcB; clientside-cookie=04188d67fa0c0a9ccb8fcbbb0bd2cb364a560243125133ccbdcff9bec51216faf6e3705dd9a14583ae45a04c42d48bc2b6bd1e0dd9229966416d6024ad37d1815ccd738ac34fea62c2dd68981e0572357e6b8cc9440d580abc08697da98cfdaa9c72f8674938908ee278f47c4fe8bcd4c4044b7d79535315a61e45491d777a28cfdf3aaff27dbbaac632580cb6834489d9fa3339792a08cb40c8b1; _fbp=fb.1.1707934690268.690152664; _tt_enable_cookie=1; _ttp=lswPB6_Kxx9sbxaw7osrD0HaIOS; ap3c=IGXNA-TQfah1UWcIAGXNA-QbZiRyWWbXzuCI6elL7AiqHG-ekQ; __adroll_fpc=a7a5a4cfd6f7f9e06203ec3fae3480f7-1707934691362; _ALGOLIA=anonymous-4b208dcc-781d-42c2-88b1-63fa46a3d18d; _gcl_au=1.1.1514012529.1707934689.1581410590.1707934777.1707934777; __public=e30%3D.GcnILYfJMKY278FQnUClucHACfVuNPNrwhUHVleAYNQ; _gid=GA1.2.1848843921.1709863828; __shopping-location=eyJzaG9wcGluZ0xvY2F0aW9uIjp7ImlkIjo1LCJuYW1lIjoiSG91c3RvbiwgVFgifX0%3D.FOFf9exESfTLmuNeml7N80put8H6NAdY3ABASvG8u1w; _hp2_ses_props.1530949394=%7B%22ts%22%3A1709887444863%2C%22d%22%3A%22www.nellisauction.com%22%2C%22h%22%3A%22%2Fsearch%22%2C%22q%22%3A%22%3Fquery%3Dhi%22%7D; _hp2_id.1530949394=%7B%22userId%22%3A%222645730681329132%22%2C%22pageviewId%22%3A%222304749522183658%22%2C%22sessionId%22%3A%222891518312091522%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga=GA1.1.807823586.1707934689; _rdt_uuid=1707934690021.bedd1a28-2cad-4ad1-a78c-25c7994cc920; ap3pages=3; __ar_v4=EQNY52S66BH4VH6D3CIXQE%3A20240215%3A4%7CXCWDW22TAVFONKHMZRMNJ5%3A20240215%3A4%7CQSXTKNUYXNCWNFQAP2WPHK%3A20240215%3A4; _ga_Z14LK6XFVL=GS1.1.1709887443.3.1.1709889544.0.0.0'}
    cookiee = get_yahoo_cookie()
    crumb_response = requests.get(
            "https://www.nellisauction.com/search?query=bose&_data=routes/search",
            headers=headers,
            allow_redirects=True,)
    # Call the API
    api_response = call_api(api_url)

    if api_response:
        print("API Response:")
        string_array = []
        avl_products_count = len(api_response['products'])
        if avl_products_count > 0 :
            avl_products = api_response['products']
            for products in avl_products:
                string_array.append(products['title'])
            print(string_array)
        else:
            print("No products")