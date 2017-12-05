import requests

r = requests.post('http://ese205soilsolutions-env.xba2aybskw.us-east-2.elasticbeanstalk.com/input', data=
{'id': '23', 'moisture': 'test 1 2 3', 'water': 'test a b c'})
print(r.status_code, r.text)