from django import forms

from rulestats.core.models import Firewall

class AdminFirewallCredentialsChangeForm(forms.ModelForm):
    """
    A form used to change a Firewalls creadentials in the admin interface.
    """
    class Meta:
        model = Firewall
        fields = ('name', 'ip', 'user', 'password', 'password2', 'enable_password', 'enable2')
        widgets = {
            'password': forms.PasswordInput(render_value=True),
            'enable_password': forms.PasswordInput(render_value=True),
        }
    
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    password2 = forms.CharField(label="Password (again)", 
                                widget=forms.PasswordInput)

    enable2 = forms.CharField(label="Enable Password (again)",
                                widget=forms.PasswordInput)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2
    
    def clean_enable2(self):
        enable1 = self.cleaned_data.get('enable_password')
        enable2 = self.cleaned_data.get('enable2')
        if enable1 and enable2:
            if enable1 != enable2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return enable2

    