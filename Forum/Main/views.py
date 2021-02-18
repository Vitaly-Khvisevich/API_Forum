from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.signals import user_logged_in

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import request, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import generics

from .serializers import UserSerializer, ArticleSerializer, CreateArticles, ArticlesDetailView, CreateComment, LikeView, AddStatistic
from .models import User, articles, comments, Like
import jwt

# Create your views here.
class CreateUserAPIView(APIView):
    """
    Рзазрешить пользователю доступ в URL
    """
    permission_classes = (AllowAny,)
  

    def post(self, request):
        user=request.data
        serializer=UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):

    try:
        email = request.data['email']
        password = request.data['password']
        user=User.objects.get(email=email, password=password)
        if user:
            try:
                payload=jwt_payload_handler(user)
                token=jwt.encode(payload, settings.SECRET_KEY)
                user_details= {}
                user_details['name']="%s %s" % (user.first_name, user.last_name)
                user_details['token']= token
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        serializer=self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = UserSerializer(request.user, data=serializer_data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer_data, status=status.HTTP_200_OK)

class Viewall(generics.ListAPIView):
    """Все опубликованные статьи"""
    serializer_class = ArticleSerializer
    queryset= articles.objects.filter(status=True)

class ArticleCreate(generics.CreateAPIView):
    """Дабавление статьи"""
    serializer_class = CreateArticles
    queryset= articles.objects.all()
    #permission_classes = (IsAuthenticated,)

class ArticleDetailView(generics.RetrieveAPIView):
    """Просмотр статьи"""
    serializer_class = ArticlesDetailView
    queryset= articles.objects.filter(status=True)

class AddComment(generics.CreateAPIView):
    """Дабавление комментария"""
    serializer_class = CreateComment
    queryset=comments.objects.all()
    permission_classes = (IsAuthenticated,)
    def perform_create(self, serializer):
        # Article is set automatically.
        serializer.save(article_id=self.kwargs.get('pk'),)


class AddLikesView(generics.CreateAPIView):
    """Добавление likes"""
    serializer_class = LikeView
    queryset=Like.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        # Article is set automatically.
        serializer.save(post_id=self.kwargs.get('pk'))

class AddStatistic(generics.RetrieveAPIView):
    """Вывод статистики по пользователю"""
    serializer_class = AddStatistic
    queryset= User.objects.all()
    permission_classes = (IsAdminUser,)