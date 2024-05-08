from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin import sites
from django.urls import resolve
from django.contrib import messages
# from django.contrib.auth import get_user_model
from .models import NoteUser
import datetime


class NotFoundRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return redirect(reverse('home'))
        return response



# class BlockUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         if request.user.is_authenticated:
#             # Check if the user is trying to access the Django admin site
#             admin_site = sites.site
#             current_resolver_match = resolve(request.path_info)
#             if current_resolver_match.app_name == admin_site.name:
#                 return response

#             try:
#                 note_user = request.user.noteuser
#             except ObjectDoesNotExist:
#                 return HttpResponseForbidden("Your account is not properly configured. Please contact support.")

#             if note_user.blocked_until and timezone.now() < note_user.blocked_until:
#                 return HttpResponseForbidden("Your account is blocked. Please try again later.")

#         return response


# class BlockUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         if request.user.is_authenticated:
#             note_user = request.user.noteuser

#             if note_user.blocked_until and timezone.now() < note_user.blocked_until:
#                 remaining_time = (note_user.blocked_until - timezone.now()).total_seconds() // 60
#                 response['X-Blocked-Message'] = f"Your account is blocked. Please try again later. Remaining time: {remaining_time} minutes."
#                 return HttpResponseForbidden(response)

#         return response

class BlockUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            try:
                note_user = request.user.noteuser
            except ObjectDoesNotExist:
                return HttpResponseForbidden("Your account is not properly configured. Please contact support.")

            if note_user.blocked_until and timezone.now() < note_user.blocked_until:
                remaining_time = (note_user.blocked_until - timezone.now()).total_seconds() // 60
                response['X-Blocked-Message'] = f"Your account is blocked. Please try again later. Remaining time: {remaining_time} minutes."
                return HttpResponseForbidden(response)

            if note_user.blocked_ip_address == request.META.get('REMOTE_ADDR'):
                remaining_time = (note_user.blocked_until - timezone.now()).total_seconds() // 60
                response['X-Blocked-Message'] = f"Your account is blocked. Please try again later. Remaining time: {remaining_time} minutes."
                return HttpResponseForbidden(response)

        return response