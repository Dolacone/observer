import sys, os
from pymiproxy.pymiproxy import *
import wc
import re, StringIO, gzip, zlib, urllib2

class DebugInterceptor(RequestInterceptorPlugin, ResponseInterceptorPlugin):

  def do_request(self, data):
    request = data.split(' ')
    host = re.search('Host:(.*?)\\r\\n', data).group(1)
    print '>> %s %s %s' % (request[0], host, request[1])
    try:
      content = data.split('\r\n\r\n')[1]
      content = re.search('data=(.*)&', content).group(1)
        
      print wc.wc_decrypt(urllib2.unquote(content))
    except:
      pass
    
    return data

  def do_response(self, data):
    try:
      # gzip format
      f = gzip.GzipFile(fileobj=StringIO.StringIO( data.split('\r\n\r\n')[1] ))
      response_data = f.read()
      
      print('<<')
      print((zlib.decompress(wc.wc_decrypt(response_data))))
    except:
      pass

    print('')    
    return data
  
  
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
        
