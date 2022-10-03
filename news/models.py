from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum, CharField
from django.core.validators import MinValueValidator
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора умножается на 3;
        p_rat = Post.objects.filter(author=self.user_id).aggregate(Sum('rating'))
        p_rat = int(list(p_rat.values())[0]) * 3
        print("p_rat", p_rat)

        # суммарный рейтинг всех комментариев автора;
        ac_rat = Comment.objects.filter(user=self.user_id).aggregate(Sum('rating'))
        ac_rat = int(list(ac_rat.values())[0])
        print("ac_rat", ac_rat)

        # суммарный рейтинг всех комментариев к статьям автора.
        ap_rat = 0
        for author_posts in Post.objects.filter(author=self.user_id):
            ap_rat += int(list(Comment.objects.filter(post=author_posts.id).aggregate(Sum('rating')).values())[0])
        print("cp_rat", ap_rat)
        self.rating = p_rat + ac_rat + ap_rat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    NEWS_TYPES = (('AR', 'статья'), ('NW', 'новость'))

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    categoryType = models.CharField(max_length=2, choices=NEWS_TYPES, default='AR')
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    text = models.TextField()
    title = models.CharField(max_length=128)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self) -> str:
        return f'{self.text[:124]}...'

    def __str__(self) -> str:
        return f'{self.title}  {self.text} rating: {self.rating}'   #{self.author.user.username}

    def get_absolute_url(self):
        # print("reverse('news', args=[str(self.id)]) = ", reverse('news', args=[str(self.id)]))
        # return reverse('news', args=[str(self.id)])
        # return reverse('news', kwargs={'pk': self.pk})
        return f'/news/{self.pk}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.categoryThrough.name}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

