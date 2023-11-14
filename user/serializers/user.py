from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "full_name")

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserSignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("Пользователь не найден")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Неправильный пароль")

        if not user.is_confirmed:
            raise serializers.ValidationError("Почта не подтвержден")

        return attrs


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password], write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "password_confirm")

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError("Поля пароля не совпадают")

        return attrs

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user


class UserConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        code = attrs.pop('code', None)
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("Пользователь не найден")

        if code != user.confirmation_code:
            raise serializers.ValidationError("Неверный пароль для подтверждение")

        return attrs

    def create(self, validated_data):
        from datetime import datetime
        user = User.objects.get(email=validated_data['email'])
        user.is_confirmed = True
        user.confirmed_date = datetime.now()
        user.save()
        return user
