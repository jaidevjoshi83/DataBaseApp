from django.utils.deprecation import MiddlewareMixin

class HSTSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Add HSTS header to response
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

# class CSPMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         response['Content-Security-Policy'] = (
#             "default-src 'self'; "
#             "script-src 'self' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
#             "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
#             "font-src 'self' https://fonts.gstatic.com data:; "
#             "connect-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com;"
#         )
#         return response