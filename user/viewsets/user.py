from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.models import Token

from user.models import User, UserFavorite
from user.serializers import (
    UserFavoriteSerializer, UserSerializer,
    UserSignInSerializer, UserSignUpSerializer,
    UserConfirmationSerializer
)


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        actions = {
            "favorite": UserFavoriteSerializer,
            "sign_in": UserSignInSerializer,
            "sign_up": UserSignUpSerializer,
            "superuser_sign_up": UserSignUpSerializer,
            "email_confirmation": UserConfirmationSerializer
        }
        if self.action in actions:
            return actions[self.action]

        return super().get_serializer_class()

    @action(detail=False, url_path="sign_in", methods=["POST"])
    def sign_in(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        password = serializer.data['password']

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

    @action(detail=False, url_path="sign_up", methods=["POST"])
    def sign_up(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.send_confirmation_code()
        return Response(serializer.data)

    @action(detail=False, url_path="superuser/sign_up", methods=["POST"])
    def superuser_sign_up(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_confirmed = True
        user.save()
        return Response(serializer.data)

    @action(detail=False, url_path="confirmation", methods=["POST"])
    def email_confirmation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, url_path="favorite", methods=["POST"], permission_classes=[IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.data["book_id"]
        user = request.user
        user_favorites, _ = UserFavorite.objects.get_or_create(user=user)
        user_favorites.books.add(book_id)
        return Response({"message": True}, status=status.HTTP_201_CREATED)
