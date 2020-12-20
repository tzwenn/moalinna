from mozilla_django_oidc.auth import OIDCAuthenticationBackend as OriginalOIDCAuthenticationBackend

def clean_email(email):
    if email:
        email = email.strip().lower()
    return email


# see https://mozilla-django-oidc.readthedocs.io/en/stable/
class OIDCAuthenticationBackend(OriginalOIDCAuthenticationBackend):

    def create_user(self, claims):
        user = super(OIDCAuthenticationBackend, self).create_user(claims)

        user.email = clean_email(claims.get('email'))
        user.username = claims.get('sub') or user.email.partition('@')[0]
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()

        return user
