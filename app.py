import os
import mod_wsgi.server

mod_wsgi-express.server.start(
  '--log-to-terminal',
  '--port', '8080',
  '--trust-proxy-header', 'X-Forwarded-For',
  '--trust-proxy-header', 'X-Forwarded-Port',
  '--trust-proxy-header', 'X-Forwarded-Proto',
  '--processes', os.environ.get('MOD_WSGI_PROCESSES', '1'),
  '--threads', os.environ.get('MOD_WSGI_THREADS', '5'),
  '--url-alias', '/static/', './static/',
  '--application-type', 'module',
  '--entry-point', 'mysite.wsgi')
