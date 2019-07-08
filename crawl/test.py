import requests
import json
import json

sess = requests.session()



response = sess.post("https://editor.geoq.cn/editormobile/proxy.do?type=GeoDataServerice&handle=filterservice/regionfilter")

print(response.text)

a = response.text

print(type(a))


a = json.loads(a)
print(a["success"])

