import os
import random
from datetime import timedelta

from django.conf import settings

from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PasswordResetOTP
from .serializers import UserSerializer
from .authentication import generate_tokens
from .permissions.internal_service import (
    IsInternalService
)
User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    role = request.data.get("role")

    if not username or not password or not email or not role:
        return Response({"error": "username, password, email, role required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=400)

    User.objects.create_user(
        username=username,
        password=password,
        email=email,
        role=role
    )

    return Response({"message": "User registered successfully"}, status=201)



@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    tokens = generate_tokens(user)

    return Response({
        "access": tokens["access"],
        "refresh": tokens["refresh"],
        "role": user.role,
        "username": user.username,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_reset_otp(request):
    email = request.data.get("email")

    if not email:
        return Response({"error": "Email is required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Email not registered"}, status=404)

    otp = str(random.randint(100000, 999999))

    PasswordResetOTP.objects.create(user=user, otp=otp)

    send_mail(
        subject="Password Reset OTP",
        message=f"Your OTP is {otp}",
        from_email=os.getenv("EMAIL_HOST_USER"),  # ✅ FIXED
        recipient_list=[email],
        fail_silently=False
    )
    return Response({"message": "OTP sent to email"})



@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_with_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")
    new_password = request.data.get("new_password")

    if not email or not otp or not new_password:
        return Response({"error": "All fields required"}, status=400)

    try:
        user = User.objects.get(email=email)
        otp_obj = PasswordResetOTP.objects.filter(
            user=user, otp=otp
        ).latest('created_at')
    except ObjectDoesNotExist:
        return Response({"error": "Invalid OTP"}, status=400)

    # 🔐 OTP Expiry Check (5 minutes)
    if otp_obj.created_at < timezone.now() - timedelta(minutes=5):
        return Response({"error": "OTP expired"}, status=400)

    user.set_password(new_password)
    user.save()

    otp_obj.delete()

    return Response({"message": "Password reset successful"})


# ============================
# LOGOUT
# ============================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    return Response({"message": "Logout successful"})


class InternalBlockUserView(APIView):
    authentication_classes = []
    permission_classes = [IsInternalService]

    def patch(self, request, user_id):

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        user.status = "blocked"
        user.save()

        return Response(
            {
                "message": "User blocked successfully"
            },
            status=status.HTTP_200_OK
        )


class InternalUnblockUserView(APIView):
    authentication_classes = []
    permission_classes = [IsInternalService]

    def patch(self, request, user_id):

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        user.status = "active"
        user.save()

        return Response(
            {
                "message": "User unblocked successfully"
            },
            status=status.HTTP_200_OK
        )


class InternalUserStatsView(APIView):
    authentication_classes = []
    permission_classes = [IsInternalService]

    def get(self, request):

        return Response({
            "total_clients": User.objects.filter(role="client").count(),
            "total_freelancers": User.objects.filter(role="freelancer").count(),
            "total_admins": User.objects.filter(role="admin").count(),
            "total_users": User.objects.count(),
        })
# ============================
# UPDATE PROFILE
# ============================
