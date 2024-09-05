import logging

from django.conf import settings
from django.contrib import auth
from django.core.cache import caches
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _

from apps.core.utils.web_utils import WebUtils

cache = caches["db"]


class KeyCloakAuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.logger = logging.getLogger(__name__)

    def process_view(self, request, view, args, kwargs):
        token = request.META.get(settings.AUTH_TOKEN_HEADER_NAME)
        if token is None:
            return WebUtils.response_401(_("please provide Token"))
        token = token.split("Bearer ")[-1]
        session_key = request.session.session_key
        if session_key:
            cache_data = cache.get(session_key)
            if cache_data:
                cache_token = cache_data["token"]
            else:
                cache_token = ""
            if cache_token == token:
                request.user.roles = cache_data["roles"]
                request.user.group_list = cache_data["group_list"]
                return None
        user = auth.authenticate(request=request, token=token)
        if user is not None:
            auth.login(request, user)
            session_key = request.session.session_key
            if not session_key:
                request.session.cycle_key()
            session_key = request.session.session_key
            data = {"token": token, "roles": user.roles, "group_list": user.group_list}
            cache.set(session_key, data, settings.LOGIN_CACHE_EXPIRED)
            # 登录成功，重新调用自身函数，即可退出
            return self.process_view(request, view, args, kwargs)
        return WebUtils.response_401(_("please provide Token"))
