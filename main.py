import requests

url = 'https://www.google.ru'

response = requests.get(url)
resp_url = response.url
headers = response.headers.get('Content-Type')
text = response.text
content = response.content

if response.status_code == 200:
    pass

if response.ok:
    pass



print(response)
