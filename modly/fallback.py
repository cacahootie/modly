from werkzeug.wrappers import BaseRequest
from werkzeug.wsgi import responder
from werkzeug.exceptions import HTTPException, NotFound

def view(request):
    raise NotFound()

@responder
def default_app(environ, start_response):
    request = BaseRequest(environ)
    try:
        return view(request)
    except HTTPException as e:
        return e
