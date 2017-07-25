from datetime import timedelta
from unittest import skip

from allauth.account.forms import BaseSignupForm
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import override_settings
from django.test.client import Client, RequestFactory
from django.utils.timezone import now
from allauth.account import app_settings
from allauth.account.models import EmailConfirmation
from allauth.account.utils import user_username
from allauth.compat import is_authenticated
from allauth.utils import get_user_model

import allauth.account.tests
import allauth.socialaccount.tests
import allauth.tests
import json


@override_settings(
    LANGUAGE_CODE='en-US'
)
class AccountTests(allauth.account.tests.AccountTests):

    @override_settings(ACCOUNT_EMAIL_CONFIRMATION_HMAC=False)
    def test_email_verification_mandatory(self):
        c = Client()
        # Signup
        resp = c.post(reverse('account_signup'), {
            'username': 'johndoe',
            'email': 'john@doe.com',
            'password1': 'johndoe',
            'password2': 'johndoe',
            'country_id': 1,
            'country_name': 'new country',
            'city_id': 1,
            'city_name': 'new city',
            'university_id': 1,
            'university_name': 'new university',
            'phone': '+78005003020'

        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(mail.outbox[0].to, ['john@doe.com'])
        self.assertGreater(mail.outbox[0].body.find('https://'), 0)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTemplateUsed(resp, 'account/verification_sent.%s' % app_settings.TEMPLATE_EXTENSION)
        # Attempt to login, unverified
        for attempt in [1, 2]:
            resp = c.post(reverse('account_login'), {
                'login': 'johndoe',
                'password': 'johndoe'
            }, follow=True)
            # is_active is controlled by the admin to manually disable
            # users. I don't want this flag to flip automatically whenever
            # users verify their email adresses.
            self.assertTrue(get_user_model().objects.filter(username='johndoe', is_active=True).exists())

            self.assertTemplateUsed(resp, 'account/verification_sent.' + app_settings.TEMPLATE_EXTENSION)
            # Attempt 1: no mail is sent due to cool-down ,
            # but there was already a mail in the outbox.
            self.assertEqual(len(mail.outbox), attempt)
            self.assertEqual(EmailConfirmation.objects.filter(email_address__email='john@doe.com').count(), attempt)
            # Wait for cooldown
            EmailConfirmation.objects.update(
                sent=now() - timedelta(days=app_settings.EMAIL_CONFIRMATION_EXPIRE_DAYS - 1, hours=23)
            )
        # Verify, and re-attempt to login.
        confirmation = EmailConfirmation.objects.filter(email_address__user__username='johndoe')[:1].get()
        resp = c.get(reverse('account_confirm_email', args=[confirmation.key]))
        self.assertTemplateUsed(resp, 'account/email_confirm.%s' % app_settings.TEMPLATE_EXTENSION)
        c.post(reverse('account_confirm_email', args=[confirmation.key]))
        resp = c.post(reverse('account_login'), {
            'login': 'johndoe',
            'password': 'johndoe'
        })
        self.assertRedirects(resp, 'http://testserver'+settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION=app_settings.EmailVerificationMethod.OPTIONAL)
    def test_optional_email_verification(self):
        c = Client()
        # Signup
        c.get(reverse('account_signup'))
        resp = c.post(reverse('account_signup'), {
            'username': 'johndoe',
            'email': 'john@doe.com',
            'password1': 'johndoe',
            'password2': 'johndoe',
            'country_id': 1,
            'country_name': 'new country',
            'city_id': 1,
            'city_name': 'new city',
            'university_id': 1,
            'university_name': 'new university',
            'phone': '+78005003020'
        })
        # Logged in
        self.assertRedirects(resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False)
        self.assertEqual(mail.outbox[0].to, ['john@doe.com'])
        self.assertEqual(len(mail.outbox), 1)
        # Logout & login again
        c.logout()
        # Wait for cooldown
        EmailConfirmation.objects.update(
            sent=now() - timedelta(days=app_settings.EMAIL_CONFIRMATION_EXPIRE_DAYS - 1, hours=23)
        )
        # Signup
        resp = c.post(reverse('account_login'), {'login': 'johndoe', 'password': 'johndoe'})
        self.assertRedirects(resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False)
        self.assertEqual(mail.outbox[0].to, ['john@doe.com'])
        # There was an issue that we sent out email confirmation mails
        # on each login in case of optional verification. Make sure
        # this is not the case:
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(ACCOUNT_LOGIN_ON_PASSWORD_RESET=True)
    def test_password_reset_ACCOUNT_LOGIN_ON_PASSWORD_RESET(self):
        user = self._request_new_password()
        body = mail.outbox[0].body
        url = body[body.find('//testserver') + len('//testserver'):].split()[0]
        resp = self.client.post(
            url,
            {'password1': 'newpass123',
             'password2': 'newpass123'})
        self.assertTrue(is_authenticated(user))
        # EmailVerificationMethod.MANDATORY sends us to the confirm-email page
        self.assertRedirects(resp, '/profile/confirm-email/')

    def test_password_reset_flow(self):
        """
        Tests the password reset flow: requesting a new password,
        receiving the reset link via email and finally resetting the
        password to a new value.
        """
        # Request new password
        user = self._request_new_password()
        body = mail.outbox[0].body
        self.assertGreater(body.find('https://'), 0)

        # Extract URL for `password_reset_from_key` view and access it
        url = body[body.find('//testserver') + len('//testserver'):].split()[0]
        resp = self.client.get(url)
        self.assertTemplateUsed(
            resp,
            'account/password_reset_from_key.%s' %
            app_settings.TEMPLATE_EXTENSION)
        self.assertFalse('token_fail' in resp.context_data)

        # Reset the password
        resp = self.client.post(url,
                                {'password1': 'newpass123',
                                 'password2': 'newpass123'})
        self.assertRedirects(resp,
                             reverse('account_reset_password_from_key_done'))

        # Check the new password is in effect
        user = get_user_model().objects.get(pk=user.pk)
        self.assertTrue(user.check_password('newpass123'))

        # Trying to reset the password against the same URL (or any other
        # invalid/obsolete URL) returns a bad token response
        resp = self.client.post(url,
                                {'password1': 'newpass123',
                                 'password2': 'newpass123'})
        self.assertTemplateUsed(
            resp,
            'account/password_reset_from_key.%s' %
            app_settings.TEMPLATE_EXTENSION)
        self.assertTrue(resp.context_data['token_fail'])

        # Same should happen when accessing the page directly
        response = self.client.get(url)
        self.assertTemplateUsed(
            response,
            'account/password_reset_from_key.%s' %
            app_settings.TEMPLATE_EXTENSION)
        self.assertTrue(response.context_data['token_fail'])

        # When in XHR views, it should respond with a 400 bad request
        # code, and the response body should contain the JSON-encoded
        # error from the adapter
        response = self.client.post(url,
                                    {'password1': 'newpass123',
                                     'password2': 'newpass123'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf8'))
        self.assertTrue('form_errors' in data)
        self.assertTrue('__all__' in data['form_errors'])

    @override_settings(
        ACCOUNT_USERNAME_REQUIRED=True,
        ACCOUNT_SIGNUP_PASSOWRD_ENTER_TWICE=True)
    def test_signup_password_twice_form_error(self):
        resp = self.client.post(
            reverse('account_signup'),
            data={
                'username': 'johndoe',
                'email': 'john@work.com',
                'password1': 'johndoe',
                'password2': 'janedoe',
                'country_id': 1,
                'country_name': 'new country',
                'city_id': 1,
                'city_name': 'new city',
                'university_id': 1,
                'university_name': 'new university',
                'phone': '+78005003020'
            }
        )
        self.assertFormError(
            resp,
            'form',
            'password2',
            'You must type the same password each time.'
        )

    @override_settings(
        ACCOUNT_USERNAME_REQUIRED=True,
        ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE=True)
    def test_signup_email_twice(self):
        request = RequestFactory().post(reverse('account_signup'), {
            'username': 'johndoe',
            'email': 'john@work.com',
            'email2': 'john@work.com',
            'password1': 'johndoe',
            'password2': 'johndoe',
            'country_id': 1,
            'country_name': 'new country',
            'city_id': 1,
            'city_name': 'new city',
            'university_id': 1,
            'university_name': 'new university',
            'phone': '+78005003020'
        })
        from django.contrib.messages.middleware import MessageMiddleware
        from django.contrib.sessions.middleware import SessionMiddleware
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)
        request.user = AnonymousUser()
        from allauth.account.views import signup
        signup(request)
        user = get_user_model().objects.get(username='johndoe')
        self.assertEqual(user.email, 'john@work.com')

    def _test_signup_email_verified_externally(self, signup_email,
                                               verified_email):
        username = 'johndoe'
        request = RequestFactory().post(reverse('account_signup'),
                                        {'username': username,
                                         'email': signup_email,
                                         'password1': 'johndoe',
                                         'password2': 'johndoe',
                                         'country_id': 1,
                                         'country_name': 'new country',
                                         'city_id': 1,
                                         'city_name': 'new city',
                                         'university_id': 1,
                                         'university_name': 'new university',
                                         'phone': '+78005003020'})
        # Fake stash_verified_email
        from django.contrib.messages.middleware import MessageMiddleware
        from django.contrib.sessions.middleware import SessionMiddleware
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)
        request.user = AnonymousUser()
        request.session['account_verified_email'] = verified_email
        from allauth.account.views import signup
        from allauth.account.adapter import get_adapter
        resp = signup(request)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'], get_adapter().get_login_redirect_url(request))
        self.assertEqual(len(mail.outbox), 0)
        return get_user_model().objects.get(username=username)


@override_settings(
    LANGUAGE_CODE='en-US'
)
class EmailFormTests(allauth.account.tests.EmailFormTests):
    pass


@override_settings(
    LANGUAGE_CODE='en-US'
)
class BaseSignupFormTests(allauth.account.tests.BaseSignupFormTests):
    @override_settings(
        ACCOUNT_USERNAME_REQUIRED=True,
        ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE=True)
    def test_signup_email_verification(self):
        data = {
            'username': 'username',
            'email': 'user@example.com',
            'country_id': 1,
            'country_name': 'new country',
            'city_id': 1,
            'city_name': 'new city',
            'university_id': 1,
            'university_name': 'new university',
            'phone': '+78005003020',
        }
        form = BaseSignupForm(data, email_required=True)
        self.assertFalse(form.is_valid())

        data = {
            'username': 'username',
            'email': 'user@example.com',
            'email2': 'user@example.com',
            'country_id': 1,
            'country_name': 'new country',
            'city_id': 1,
            'city_name': 'new city',
            'university_id': 1,
            'university_name': 'new university',
            'phone': '+78005003020',
        }
        form = BaseSignupForm(data, email_required=True)
        self.assertTrue(form.is_valid())

        data['email2'] = 'anotheruser@example.com'
        form = BaseSignupForm(data, email_required=True)
        self.assertFalse(form.is_valid())

    @override_settings(
        ACCOUNT_USERNAME_REQUIRED=True,
        ACCOUNT_USERNAME_BLACKLIST=['username'])
    def test_username_in_blacklist(self):
        data = {
            'username': 'username',
            'email': 'user@example.com',
            'country_id': 1,
            'country_name': 'new country',
            'city_id': 1,
            'city_name': 'new city',
            'university_id': 1,
            'university_name': 'new university',
            'phone': '+78005003020',
        }
        form = BaseSignupForm(data, email_required=True)
        self.assertFalse(form.is_valid())

    @override_settings(
        ACCOUNT_USERNAME_REQUIRED=True,
        ACCOUNT_USERNAME_BLACKLIST=['username'])
    def test_username_not_in_blacklist(self):
        data = {
            'username': 'theusername',
            'email': 'user@example.com',
            'country_id': 1,
            'country_name': 'new country',
            'city_id': 1,
            'city_name': 'new city',
            'university_id': 1,
            'university_name': 'new university',
            'phone': '+78005003020',
        }
        form = BaseSignupForm(data, email_required=True)
        self.assertTrue(form.is_valid())


class AuthenticationBackendTests(allauth.account.tests.AuthenticationBackendTests):
    pass


class UtilsTests(allauth.account.tests.UtilsTests):
    pass


class BaseTest(allauth.tests.BasicTests):
    pass


class SocialAccountTests(allauth.socialaccount.tests.SocialAccountTests):
    @override_settings(
        ACCOUNT_EMAIL_REQUIRED=True,
        ACCOUNT_UNIQUE_EMAIL=True,
        ACCOUNT_USERNAME_REQUIRED=True,
        ACCOUNT_AUTHENTICATION_METHOD='email',
        SOCIALACCOUNT_AUTO_SIGNUP=True)
    def test_email_address_clash_username_required(self):
        """Test clash on both username and email"""
        request, resp = self._email_address_clash('test', 'test@test.com')
        self.assertEqual(resp['location'], reverse('main:index'))

    @override_settings(
        ACCOUNT_EMAIL_REQUIRED=True,
        ACCOUNT_UNIQUE_EMAIL=True,
        ACCOUNT_USERNAME_REQUIRED=False,
        ACCOUNT_AUTHENTICATION_METHOD='email',
        SOCIALACCOUNT_AUTO_SIGNUP=True)
    def test_email_address_clash_username_not_required(self):
        """Test clash while username is not required"""
        request, resp = self._email_address_clash('test', 'test@test.com')
        self.assertEqual(resp['location'], reverse('main:index'))


    @override_settings(
        ACCOUNT_EMAIL_REQUIRED=True,
        ACCOUNT_UNIQUE_EMAIL=True,
        ACCOUNT_USERNAME_REQUIRED=False,
        ACCOUNT_AUTHENTICATION_METHOD='email',
        SOCIALACCOUNT_AUTO_SIGNUP=True)
    def test_email_address_clash_username_auto_signup(self):
        # Clash on username, but auto signup still works
        request, resp = self._email_address_clash('test', 'other@test.com')
        self.assertEqual(resp['location'], reverse('profile:edit'))
        user = get_user_model().objects.get(**{app_settings.USER_MODEL_EMAIL_FIELD: 'other@test.com'})
        self.assertNotEqual(user_username(user), 'test')

    @skip
    def test_unique_email_validation_signup(self):
        pass

    @skip
    def test_unverified_email_change_at_signup(self):
        pass

    @skip
    def test_verified_email_change_at_signup(self):
        pass
