import sys, os
from pymiproxy.pymiproxy import *

class DebugInterceptor(RequestInterceptorPlugin, ResponseInterceptorPlugin):

  def do_request(self, data):
    return data

  def do_response(self, data):
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
        
