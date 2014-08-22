observer
=======

`observer` allows user to hook their python plugin easily.

### observer plugin template

```python
from pymiproxy.pymiproxy import *

class DebugInterceptor(RequestInterceptorPlugin, ResponseInterceptorPlugin):
  def do_request(self, data):
    print("request data: %s" % (data))
    return data

  def do_response(self, data):
    print("response data: %s" % (data))
    return data
    
if __name__ == '__main__':
  proxy = None
  proxy = AsyncMitmProxy()
  proxy.register_interceptor(DebugInterceptor)
  try:
    proxy.serve_forever()
  except KeyboardInterrupt:
    proxy.server_close()
```

### Run proxy
```bash
$ python plugin.py
```
Proxy will start with 0.0.0.0:8000
