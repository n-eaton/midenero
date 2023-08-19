from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render( request, 'auth/register.html')
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        context = {
            'fieldValues': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
        
                if len(password) < 8:
                    messages.error(request, 'The password should be at least 8 characters',context)
                    return render( request, 'auth/register.html')
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active=False
                user.save()
                email_subject = 'Activate your account'
                email_body= 'only for the test'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "neaton278@hotmail.com",
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account is created')
                return render( request, 'auth/register.html')                
                
        # messages.success(request,'Success. Congratulations! ')
        # messages.warning(request,'Success. Congratulations! warning ')
        # messages.info(request,'Success. Congratulations! info')
        # messages.error(request,'Success. Congratulations! error')

        return render( request, 'auth/register.html')
    
class UserNameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'The username is taken. Please choose another one'}, status=409)
        
        
        return JsonResponse({'username_valid': True})
    
class EmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'This email is taken. Please choose another one'}, status=409)
        
        
        return JsonResponse({'email_valid': True})