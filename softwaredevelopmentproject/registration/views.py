from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def register(request):
    if request.method == 'POST':
        account_id = request.POST.get('accountid')
        password = request.POST.get('password')

        # Check if account ID already exists
        if User.objects.filter(account_id=account_id).exists():
            messages.error(request, 'Account already registered.')
            return render(request, 'registration/register.html')

        # Encrypt the password
        encrypted_password = make_password(password)

        # Create new user without first and last name
        User.objects.create(
            account_id=account_id,
            password=encrypted_password  # store the hashed password
        )

        # Notify user of successful registration
        messages.success(request, 'Registration successful. Please login.')

        return redirect('login')  # Redirect to the login page

    return render(request, 'registration/register.html')

def login(request):
    if request.method == 'POST':
        account_id = request.POST.get('accountid')
        password = request.POST.get('password')
        user = User.objects.filter(account_id=account_id).first()

        if user and check_password(password, user.password):
            # Assuming you have session handling or some other auth mechanism
            request.session['user_id'] = user.id  # Simple example of setting a session
            return redirect('profile_management')  # Redirect to a profile or home page
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'registration/login.html')

def profile_management(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login if no session found

    user = User.objects.get(id=user_id)
    
    context = {
        'user': user,
        'initial': user.account_id[0].upper()
    }

    return render(request, 'registration/profile_management.html', context)  # Render the page for GET requests


def placeholder_function(request):
    # Perform some action or just pass
    messages.info(request, 'This function is not yet implemented.')
    return redirect('login')




def change_password(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if check_password(old_password, user.password):
            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Your password has been successfully changed.', extra_tags='success')
                return render(request, 'registration/change_password.html')
            else:
                messages.error(request, 'New passwords do not match.', extra_tags='error')
        else:
            messages.error(request, 'Your old password was entered incorrectly.', extra_tags='error')

    return render(request, 'registration/change_password.html')