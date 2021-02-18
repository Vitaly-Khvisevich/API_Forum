from rest_framework import serializers
from.models import User, articles, spheres, Like, comments


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class AuthorCoordinateSerializer(serializers.Serializer):
    """Вывод полной информации по автору"""
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    email = serializers.EmailField(source='author.email')

class SphereSerializer(serializers.ModelSerializer):
    """Вывод полной информации по сфере"""
    class Meta:
        model = spheres
        fields = ('name',)

class ArticleSerializer(serializers.ModelSerializer):
    """Вывод всех опубликованных статей"""
    author=AuthorCoordinateSerializer(source='*')
    sphere=SphereSerializer(many=True)
    class Meta(object):
        model = articles
        fields = ('id', 'title','author', 'created_at', 'sphere')

class CreateArticles(serializers.ModelSerializer):
    """Создание статьи"""
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta(object):
        model = articles
        fields = ('title','author', 'topic', 'sphere', 'body')

class investedcomment(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class ArticleCommentView(serializers.ModelSerializer):
    """Вывод комментариев"""
    author=AuthorCoordinateSerializer(source='*')
    children=investedcomment(many=True)
    class Meta(object):
        list_serializer_class = FilterReviewListSerializer
        model = comments
        fields =('id','author','text','children')

class ArticlesDetailView(serializers.ModelSerializer):
    """Детальная информация по выбранной статье"""
    author=AuthorCoordinateSerializer(source='*')
    sphere=SphereSerializer(many=True)
    comments=ArticleCommentView(many=True)
    rating = serializers.SerializerMethodField(method_name='rating_count')
    def rating_count(self, object):
        """Подсчет количества likes и dislikes"""
        rating={}
        like=0
        dislike=0
        for i in Like.objects.filter(post=object.pk):
            if i.like == 'like':
                like+=1
            else:
                dislike+=1
        rating['Like']=like
        rating['Dislike']=dislike
        return rating
    class Meta(object):
        model = articles
        fields = ('title','created_at','author', 'topic', 'sphere', 'body', 'comments', 'rating' )

class CreateComment(serializers.ModelSerializer):
    """Добавление комментария"""
  
    class Meta(object):
        model = comments
        fields = ('author', 'text', 'parent', )

class LikeView(serializers.ModelSerializer):
    """Вывод информации по likes"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta(object):
        model = Like
        fields = ('user', 'like')



class AddStatistic(serializers.ModelSerializer):
    """Вывод статистики по пользователю"""
    article_author = serializers.SerializerMethodField(method_name='rating_count')
    def rating_count(self, object):
        """Подсчет количества коментариев, likes и dislikes"""
        rating={}
        lencoments=0
        article={}
        like=0
        dislike=0
        for i in articles.objects.filter(author=object.pk):
            for j in comments.objects.filter(article=i.id):
                lencoments+=1
            for k in Like.objects.filter(post=i.id):
                if k.like == 'like':
                    like+=1
                else:
                    dislike+=1
            rating['Comments']=lencoments
            rating['Like']=like
            rating['Dislike']=dislike
            article[i.title]=rating
            rating ={}   
        
        return article
    class Meta(object):
        model = User
        fields = ('first_name','last_name','email', 'date_joined', 'article_author')