from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from django.urls import reverse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from . models import User


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        if not sociallogin.user.email:
            raise OAuth2Error('Для авторицации необходимо дать доступ к электронному адресу')
        try:
            user = User.objects.get(email=sociallogin.user.email)
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            sociallogin.state['next'] = reverse('profile:edit', args=[sociallogin.user.id])
