from allauth.account.forms import LoginForm, get_adapter, app_settings

from django.utils.translation import pgettext, ugettext, ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User

from users.models import SubscriberEmail


class SubscriberEmailForm(forms.ModelForm):
    class Meta:
        model = SubscriberEmail
        fields = ['email']


class Login(LoginForm):
    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        login_widget = forms.TextInput(attrs={'type': 'email',
                                              'placeholder':
                                                  _('E-mail address'),
                                              'autofocus': 'autofocus'})
        login_field = forms.EmailField(label=_("E-mail"),
                                       widget=login_widget)
        self.fields["login"] = login_field

    def clean(self):
        super(LoginForm, self).clean()
        if self._errors:
            return
        credentials = self.user_credentials()

        try:
            username = User.objects.get(email=credentials['email']).username
            credentials['username'] = username
            del credentials['email']
        except User.DoesNotExist:
            pass

        user = get_adapter(self.request).authenticate(
            self.request,
            **credentials)
        if user:
            self.user = user
        else:
            auth_method = app_settings.AUTHENTICATION_METHOD
            if auth_method == app_settings.AuthenticationMethod.USERNAME_EMAIL:
                login = self.cleaned_data['login']
                if self._is_login_email(login):
                    auth_method = app_settings.AuthenticationMethod.EMAIL
                else:
                    auth_method = app_settings.AuthenticationMethod.USERNAME
            raise forms.ValidationError(
                self.error_messages['%s_password_mismatch' % auth_method])
        return self.cleaned_data