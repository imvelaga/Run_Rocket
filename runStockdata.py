import requests

url = 'http://query1.finance.yahoo.com/v1/test/getcrumb'
response = requests.get(url)
print('Hi  ',response)