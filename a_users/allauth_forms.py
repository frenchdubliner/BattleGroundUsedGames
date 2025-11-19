from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField

class CustomSignupForm(SignupForm):
    captcha = CaptchaField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make captcha field required
        self.fields['captcha'].required = True

