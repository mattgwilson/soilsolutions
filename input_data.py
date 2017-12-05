import requests

r = requests.post('http://ese205soilsolutions-env.xba2aybskw.us-east-2.elasticbeanstalk.com/input', data=
{'id': 'test1', 'moisture': 'test2', 'water': 'test3'})
print(r.status_code, r.text)

"""This code is in the python code we run for our project with different values for ID, Moisture, and Water"""
