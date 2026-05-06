"""
URL configuration for authservice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf import settings
from myapp import  views
from django.conf.urls.static import static
urlpatterns = [
    path('register/',views.register_view),
    path('login/',views.login_view),
    path('profile/',views.profile_view),
    path('password-reset/otp/',views.send_reset_otp),
    path('password-reset/confirm/',views.reset_password_with_otp),
    path('logout/',views.logout_view),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

