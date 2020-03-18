import logging
from django.conf import settings

from mozilla_django_oidc.auth import OIDCAuthenticationBackend


logger = logging.getLogger(__name__)


class XorgAuthenticationBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        logger.info("Verifying claims %r", claims)
        # Verify that the required group is in xorg_groups
        xorg_groups = claims.get("x_groups")
        forlife = claims.get("sub")
        if not xorg_groups or not forlife:
            return False
        result = settings.XORGAUTH_REQUIRED_GROUP in xorg_groups
        if not result:
            logger.info("Failed to verify claims %r (expecting group %r)", claims, settings.XORGAUTH_REQUIRED_GROUP)
            print(repr(settings.XORGAUTH_WHITELISTED_USERS))
            if forlife in settings.XORGAUTH_WHITELISTED_USERS:
                logger.info("... but user has been whitelisted")
                result = True
        return result

    def create_user(self, claims):
        logger.info("Creating user for claims %r", claims)
        forlife = claims.get("sub")
        return self.UserModel.objects.create_user(forlife)

    def filter_users_by_claims(self, claims):
        logger.info("Getting user for claims %r", claims)
        forlife = claims.get("sub")
        if not forlife:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(username=forlife)
