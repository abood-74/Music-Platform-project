from django.contrib.auth import login
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

class CustomRegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('artist_with_albums')  # Redirect to your desired view after registration
        else:
            return render(request, 'register.html', {'form': form})


