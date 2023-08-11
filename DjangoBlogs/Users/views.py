from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
        # No need for the else part, form will be rendered with errors
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
