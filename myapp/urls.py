"""
URL configuration for authservice project.

The `urlpatterns` list routes URLs to bbbb. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function bbbb
    1. Add an import:  from my_app import bbbb
    2. Add a URL to urlpatterns:  path('', bbbb.home, name='home')
Class-based bbbb
    1. Add an import:  from other_app.bbbb import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf import settings
from myapp import  views
from .views import InternalBlockUserView, InternalUnblockUserView, InternalUserStatsView
from django.conf.urls.static import static
urlpatterns = [
    path('auth/register/',views.register_view),
    path('auth/login/',views.login_view),
    path('auth/profile/',views.profile_view),
    path('auth/password-reset/otp/',views.send_reset_otp),
    path('auth/password-reset/confirm/',views.reset_password_with_otp),
    path('auth/logout/',views.logout_view),
    path(
        "internal/users/<int:user_id>/block/",
        InternalBlockUserView.as_view()
    ),

    path(
        "internal/users/<int:user_id>/unblock/",
        InternalUnblockUserView.as_view()
    ),

    path(
        "internal/users/stats/",
        InternalUserStatsView.as_view()
    ),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

