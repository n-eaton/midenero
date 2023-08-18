from .views import RegistrationView, UserNameValidation, EmailValidation
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path('validate-username',csrf_exempt(UserNameValidation.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidation.as_view()), name="validate_email"),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)