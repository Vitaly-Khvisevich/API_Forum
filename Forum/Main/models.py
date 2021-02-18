from __future__ import unicode_literals
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)

# Create your models here.
class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Создает пользователя при введенном Email и пароле.
        """
        if not email:
            raise ValueError('Введите Email')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Абстрактный базовый класс реализующий модель пользователя
    """
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

class articles(models.Model):
    """
    Статьи
    """
    title = models.CharField('article title',max_length=120)
    created_at = models.DateTimeField("article data", auto_now=True)
    author =models.ForeignKey('User', related_name='article_author', on_delete=models.CASCADE)
    topic = models.CharField('article topic',max_length=120)
    sphere = models.ManyToManyField('spheres', related_name='article_sphere')
    body = models.TextField('article body')
    status = models.BooleanField('is_published',default=False)

    def __str__(self):
        return (f"{self.title} - {self.topic}")

class spheres(models.Model):
    """
    Сфера статьи
    """
    name = models.CharField('sphare name',max_length=200, help_text="Enter a article sphere ")

    def __str__(self):
        return self.name

class comments(models.Model):
    """Отзывы"""
    author =models.ForeignKey('User', related_name='comment_author', on_delete=models.CASCADE)
    text = models.TextField("comment text", max_length=5000)
    parent = models.ForeignKey('self', verbose_name='parent comment',on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    article = models.ForeignKey('articles', verbose_name='comment article', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.author} - {self.article}"

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

class Like(models.Model):
    """Like model"""
    LIKE = (
        ('like', 'like'),
        ('dislike', 'dislike')
    )

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('articles', on_delete=models.CASCADE, related_name='likes')
    like = models.CharField(max_length=255, choices=LIKE)
    