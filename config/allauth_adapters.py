"""Module for custom django-allauth adapters."""
from django.contrib.auth import get_user_model

from annoying.functions import get_object_or_None

from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.utils import user_email
from allauth.socialaccount import app_settings as socialaccount_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.twitter.provider import TwitterProvider


class AutoconnectSocialAccountAdapter(DefaultSocialAccountAdapter):

    """Adapter that allows autoconnect accounts based on e-mail address.

    Only allows this for the selected providers which claim that they
    don't return e-mail addresses that weren't verified (e.g. Twitter).
    """

    def should_allow_autoconnect_by_email(self, sociallogin):
        """Allow autoconnect only for selected platforms.

        Not on all platforms e-mails are verified.
        """
        return sociallogin.account.provider == TwitterProvider.id

    def new_user(self, request, sociallogin):
        """Get or create User by emails from `sociallogin`.

        Differs from the parent method in that it returns a User from
        the DB if one with any of the `sociallogin.email_addresses`
        if such exists.
        """
        if not self.should_allow_autoconnect_by_email(sociallogin):
            return super(AutoconnectSocialAccountAdapter,
                         self).new_user(request, sociallogin)

        user_model = get_user_model()
        for email_address in sociallogin.email_addresses:
            user = get_object_or_None(user_model, email=email_address.email)
            if user:
                return user
        return user_model()

    def save_user(self, request, sociallogin, form=None):
        """Save a newly signed up social login.

        Only invoked during signup.

        Differs from the parent method in that:
            1) Saves `sociallogin` in `connect` mode.
            2) Sets `username` to be equal to `email` where the parent
                method would call
                `get_account_adapter().populate_username`.
        """
        if not self.should_allow_autoconnect_by_email(sociallogin):
            return super(AutoconnectSocialAccountAdapter,
                         self).save_user(request, sociallogin, form)

        u = sociallogin.user
        u.set_unusable_password()
        if form:
            get_account_adapter().save_user(request, u, form)
        else:
            u.username = u.email
        sociallogin.save(request, connect=True)
        return u

    def is_auto_signup_allowed(self, request, sociallogin):
        """Whether auto signup is allowed.

        Differs from the parent method in that it additionally allows
        autoconnect of a social account to an existing User by e-mail.
        """
        if not self.should_allow_autoconnect_by_email(sociallogin):
            return super(AutoconnectSocialAccountAdapter,
                         self).is_auto_signup_allowed(request, sociallogin)

        auto_signup = socialaccount_settings.AUTO_SIGNUP
        if auto_signup and socialaccount_settings.EMAIL_REQUIRED and \
                not user_email(sociallogin.user):
            auto_signup = False
        return auto_signup
