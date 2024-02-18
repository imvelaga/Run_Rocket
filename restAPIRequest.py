import requests

def call_api(url, params=None):
    """
    Function to call a REST API and return the response.

    Args:
    - url: The URL of the API endpoint.
    - params: Optional parameters to be sent with the request.

    Returns:
    - Response object.
    """
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
    api_url = "https://www.nellisauction.com/search?query=bose&_data=routes%2Fsearch"

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