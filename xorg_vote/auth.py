from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class XorgAuthenticationBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        xorg_groups = claims.get("xorg_groups")
        return bool(xorg_groups)

    def create_user(self, claims):
        forlife = claims.get("sub")
        return self.UserModel.objects.create_user(forlife)

    def filter_users_by_claims(self, claims):
        forlife = claims.get("sub")
        if not forlife:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(username=forlife)
