from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm

User = get_user_model()


class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request):
        context = {
            'form': CustomUserCreationForm()
        }
        return render(
            request,
            self.template_name,
            context
        )

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = email.replace('@', '', 1)
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username, email, password)
            user.save()
            user = authenticate(username=email, password=password)
            login(request, user)
            return redirect('index')
        context = {
            'form': form,
        }
        return render(
            request,
            self.template_name,
            context
        )
