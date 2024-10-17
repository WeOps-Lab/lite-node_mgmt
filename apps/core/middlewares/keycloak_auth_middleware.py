import logging

from django.conf import settings
from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _

from apps.core.utils.web_utils import WebUtils
from config.default import DEBUG


class KeyCloakAuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.logger = logging.getLogger(__name__)

    def process_view(self, request, view, args, kwargs):
        # 开发模式，放行swagger
        if DEBUG is True:
            if request.path.startswith("/swagger"):
                return None

        # 开放接口，不需要认证
        if request.path.startswith('/open_api/'):
            return None

        token = request.META.get(settings.AUTH_TOKEN_HEADER_NAME)
        if token is None:
            return WebUtils.response_401(_("please provide Token"))
        token = token.split("Bearer ")[-1]
        user = auth.authenticate(request=request, token=token)
        if user is not None:
            auth.login(request, user)
            session_key = request.session.session_key
            if not session_key:
                request.session.cycle_key()
            # 登录成功，重新调用自身函数，即可退出
            return None
        return WebUtils.response_401(_("please provide Token"))
