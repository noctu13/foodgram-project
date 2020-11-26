from django.views.generic import CreateView
from .forms import SignUpForm


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = "/auth/login/"
    template_name = "signup.html"
