from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User


def issue_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


from rest_framework import serializers


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "name", "phone", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)


import phonenumbers


def normalize_phone(phone: str, default_region: str = "IN") -> str | None:
    try:
        parsed = phonenumbers.parse(phone, default_region)
        if not phonenumbers.is_possible_number(parsed) or not phonenumbers.is_valid_number(parsed):
            return None
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except Exception:
        return None


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.copy()
        norm = normalize_phone(data.get("phone", ""))
        if not norm:
            return Response({"detail": "Invalid phone"}, status=status.HTTP_400_BAD_REQUEST)
        data["phone"] = norm
        serializer = SignupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": SignupSerializer(user).data, "tokens": issue_tokens(user)}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = normalize_phone(serializer.validated_data["phone"])
        if not phone:
            return Response({"detail": "Invalid phone"}, status=status.HTTP_400_BAD_REQUEST)
        password = serializer.validated_data["password"]
        user = authenticate(request, phone=phone, password=password)
        if user:
            return Response({"tokens": issue_tokens(user)}, status=status.HTTP_200_OK)
        try:
            existing = User.objects.get(phone=phone)
            return Response({"detail": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create(name=phone, phone=phone)
            user.set_password(password)
            user.save()
            return Response({"user": SignupSerializer(user).data, "tokens": issue_tokens(user)}, status=status.HTTP_201_CREATED)

# Create your views here.
