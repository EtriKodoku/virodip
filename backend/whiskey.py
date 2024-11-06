from validation import validate_token

# Middleware class
class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(environ, "fgfhjff", start_response)
        print(f"Incoming request to {environ['PATH_INFO']}")
        return self.app(environ, start_response)

