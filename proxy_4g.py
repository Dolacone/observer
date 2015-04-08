import sys, os
from pymiproxy.pymiproxy import *
import re, StringIO, gzip, zlib, urllib2, json, httplib

_cookie = ""
_body = "" 

class DebugInterceptor(RequestInterceptorPlugin, ResponseInterceptorPlugin):

  def do_request(self, data):
    print data
    if data.find('POST /api/items/whistle.json') == 0:
      updateTemplate(data)
    return data

  def do_response(self, data):
    # seperate response into header and body
    retData = data.split('\r\n\r\n')
    enemyGroup = parse_enemyGroup( parse_response(retData[1]) )

    if not enemyGroup:
      # return if not battle format
      return retData

    while not enemyGroup > 5000:
      # resend battle trigger if not turtle
      print enemyGroup
      battle_finish()
      retData[1] = battle_init()
      enemyGroup = parse_enemyGroup( parse_response(retData[1]) )

    print enemyGroup
    # replace content-length with new body
    retData[0] = re.sub(r"(Content-Length:) \d+", r"\1 " + str(len(retData[1])), retData[0])
    return '\r\n\r\n'.join(retData)
  
def updateTemplate(data):
  global _body, _cookie
  _cookie = re.search("Cookie: (.*)\n", data).group(1)
  _body = data.split('\r\n\r\n')[1]
  
def parse_response(data):
  f = gzip.GzipFile(fileobj=StringIO.StringIO( data ))
  return f.read()
  
def parse_enemyGroup(data):
  try:
    content = json.loads(data)
    return content["response"]["body"]["info"]["battle"]["enemy_group_code"]
  except:
    return None
  
def enemy_match(data, enemy_list):
  pass
  
def battle_init():
  return kakuriyo_request('/api/items/whistle.json')

def battle_finish():
  return kakuriyo_request('/api/battles/finish.json')

def kakuriyo_request(path):
  conn = httplib.HTTPConnection("s1.kakuriyo-no-mon.com")
  kakuriyo_header = {
    "Host": "s1.kakuriyo-no-mon.com",
    "Proxy-Connection": "keep-alive",
    "Origin": "http://s1.kakuriyo-no-mon.com",
    "X-Requested-With": "ShockwaveFlash/17.0.0.134",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Referer": "http://s1.kakuriyo-no-mon.com/swf/kagura_main.swf?v=20150401101501",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-TW,zh;q=0.8,ja;q=0.6,en-US;q=0.4,en;q=0.2,zh-CN;q=0.2",
    "Cookie": _cookie,
  }
      
  conn.request("POST", path, _body, headers=kakuriyo_header)
  response = conn.getresponse()
  return response.read()

if __name__ == '__main__':
  proxy = None
  if not sys.argv[1:]:
    proxy = AsyncMitmProxy()
  else:
    proxy = AsyncMitmProxy(ca_file=sys.argv[1])
  proxy.register_interceptor(DebugInterceptor)
  try:
    proxy.serve_forever()
  except KeyboardInterrupt:
    proxy.server_close()
        
