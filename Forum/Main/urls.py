
from django.urls import path
from .views import CreateUserAPIView, authenticate_user, UserRetrieveUpdateAPIView, Viewall, ArticleCreate, ArticleDetailView, AddComment, AddLikesView, AddStatistic

urlpatterns = [
    path('user/create/', CreateUserAPIView.as_view()),
    path('user/obtain_token/', authenticate_user),
    path('user/update/', UserRetrieveUpdateAPIView.as_view()),
    path('article/all/', Viewall.as_view()),
    path('article/create/', ArticleCreate.as_view() ),
    path('article/<int:pk>/', ArticleDetailView.as_view() ),
    path('article/<int:pk>/addcomment/', AddComment.as_view() ),
    path("article/<int:pk>/rating/", AddLikesView.as_view()),
    path("statistic/user/<int:pk>/", AddStatistic.as_view()),

]