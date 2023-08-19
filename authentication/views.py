from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth

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
                
                # path to view
                # # - encode uid
                # uidb64 = force_bytes(urlsafe_base64_encode(user.pk))
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                # - getting domain we are on
                domain = get_current_site(request).domain
                
                # - relative url to verification
                link = reverse('activate', kwargs = {
                    'uidb64': uidb64, 'token':token_generator.make_token(user)
                    })
                
                activate_url='http://'+ domain + link
                # - token
                
                email_subject = 'Activate your account'
                email_body= 'Hi there, ' + user.username + '! Please use this link to verify your email\n\n'+ activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "neaton278@hotmail.com",
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account is created')
                
                return render( request, 'auth/register.html')                
                


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



class VerificationView(View):
    def get(self, request, uidb64, token):
        
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not token_generator.check_token(user, token):
                return redirect('login'+ '?message'+'User already activated')
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            
            messages.success(request, 'Your account is now activated')
            return redirect('login')
        except Exception as ex:
            pass
        
        
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request,'auth/login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, '+ user.username + ' You are logged in ')
                    return redirect('expenses') 
                messages.error(request, 'Account is not active. Please check your email')
                return render(request,'auth/login.html')  
            
            messages.error(request, 'Try again. Invalid credentials')
            return render(request,'auth/login.html')  

        messages.error(request, 'Please filled out the fields correctly')
        return render(request,'auth/login.html')  
           
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return render(request,'auth/login.html')
    