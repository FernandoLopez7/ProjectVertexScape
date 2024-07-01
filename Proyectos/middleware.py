# import mimetypes

# class GZipMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         if request.path.endswith('.gz'):
#             response['Content-Encoding'] = 'gzip'
#             response['Content-Type'] = mimetypes.guess_type(request.path)[0]

#         return response

# from django.conf import settings
# from django.utils.deprecation import MiddlewareMixin

# class DisableCSRFMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.path.startswith(settings.ADMIN_URL) and getattr(request, 'method', None) == 'POST':
#             setattr(request, '_dont_enforce_csrf_checks', True)
