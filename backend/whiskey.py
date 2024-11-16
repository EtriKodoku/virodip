from validation import validate_token
from werkzeug.wrappers import Response


class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
            #  OPTIONS is used for preflight check for CORS
            print(environ)
            if environ.get('REQUEST_METHOD') == "OPTIONS" or 'public' in environ.get('RAW_URI') :
                return self.app(environ, start_response)
            else:
                try:
                    auth_header = environ.get('HTTP_AUTHORIZATION', '')
                    if auth_header.startswith("Bearer "):
                        token = auth_header.replace("Bearer ", "")
                        token_data = validate_token(token)
                        environ['token_data'] = token_data
                    else:
                        raise ValueError("No Bearer token found")
                except Exception as e:
                    # Token is invalid or not provided, return 401 response
                    response = Response(
                        response='{"error": "Unauthorized"}',
                        status=401,
                        content_type="application/json"
                    )
                    return response(environ, start_response)

                print(f"Incoming request to {environ['PATH_INFO']} with token_data: {environ.get('token_data')}")
                return self.app(environ, start_response)