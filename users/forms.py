from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    class Meta():
        model = get_user_model()
        fields = ("first_name", "username", "email")
