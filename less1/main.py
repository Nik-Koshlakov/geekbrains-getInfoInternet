import requests
import json
import base64

# task 1
    # getting github repos for user
user_name = 'Nik-Koshlakov'
url = f'https://api.github.com/users/{user_name}/repos'
response = requests.get(url)
data = json.loads(response.text)

with open('data.json', 'w') as f:
    json.dump(data, f, indent=5)

print('repos:')
for el in data:
    print(el['full_name'])


# task 2
url = 'https://api.notion.com/v1/pages/4316410de9ea421189299545fe4d3e8f'
headers = {'Authorization': 'Bearer secret_WwResFV3b5ZJFsLXyX2s7jJcVlIHtYkGv9fDdKnNZEc',
           'Notion-Version': '2021-08-16'}
response = requests.get(url, headers=headers)
data = json.loads(response.text)

with open('data2.json', 'w') as f:
    json.dump(dict(response.headers), f, indent=5)

print("\n" + response.headers)
print(data)