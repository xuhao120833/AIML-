import json,urllib
from urllib.parse import urlencode
import urllib.request

url = 'http://api.k780.com'
params = {
  'app' : 'weather.today',
  'weaid' : 'zhenjiang',
  'appkey' : '55198',
  'sign' : '41c4453f512e07ba8c808a1d1569cc38',
  'format' : 'json',
}
params = urlencode(params)

f = urllib.request.urlopen('%s?%s' % (url, params))
nowapi_call = f.read()
#print content
a_result = json.loads(nowapi_call)
if a_result:
  if a_result['success'] != '0':
    print(a_result['result']['weather_icon'])
  else:
    print (a_result['msgid']+' '+a_result['msg'])
else:
  print ('Request nowapi fail.')