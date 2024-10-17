import logging
import traceback

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import translation

from apps.core.utils.keycloak_client import KeyCloakClient

logger = logging.getLogger("app")


class KeycloakAuthBackend(ModelBackend):
    def authenticate(self, request=None, username=None, password=None, token=None):
        if settings.DEBUG:
            default_user = {"username": "admin", "name": "admin", "email": "admin@admin.com"}
            groups = [{"id": "2135b2b5-cbb4-4aea-8350-7329dcb6671a", "name": "admin"}]
            translation.activate("zh-Hans")
            return self.set_user_info(groups, ["admin"], default_user)
        logger.debug("Enter in TokenBackend")
        # 判断是否传入验证所需的bk_token,没传入则返回None
        if not token:
            return None
        client = KeyCloakClient()
        is_active, user_info = client.token_is_valid(token)
        # 判断bk_token是否验证通过,不通过则返回None
        if not is_active:
            return None
        if user_info.get("locale"):
            translation.activate(user_info["locale"])
        roles = user_info["realm_access"]["roles"]
        groups = client.get_user_groups(user_info["sub"], "admin" in roles)
        return self.set_user_info(groups, roles, user_info)

    @staticmethod
    def set_user_info(groups, roles, user_info):
        try:
            user, _ = User.objects.get_or_create(username=user_info["username"])
            user.email = user_info.get("email", "")
            user.is_superuser = "admin" in roles
            user.is_staff = user.is_superuser
            user.save()
            user.group_list = groups
            user.roles = roles
            user.locale = user_info.get("locale", "zh-Hans")
            return user
        except IntegrityError:
            logger.exception(traceback.format_exc())
            logger.exception("get_or_create UserModel fail or update_or_create UserProperty")
            return None
        except Exception:
            logger.exception(traceback.format_exc())
            logger.exception("Auto create & update UserModel fail")
            return None
