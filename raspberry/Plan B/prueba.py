import requests

req = requests.get("http://172.16.66.84:8084/Senint2/serverB")
req.encoding
print(req.status_code)
#print(req.)