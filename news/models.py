from django.db import models
from django.contrib.auth.models import User




class Author(models.Model):
    rating = models.IntegerField(default=0)
    author = models.OneToOneField(User, on_delete=models.CASCADE)

        def update_rating(self, last_rating):
            self.rating = last_rating
            self.save()
        


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)


article = 'AR'
news = 'NE'

CHOICE = [
           (article, 'Статья'),
           (news, 'Новости')
         ]


class Post(models.Model):
    objects = None
    text = models.TextField()
    heading = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    datetime_post = models.DateTimeField(auto_now_add=True)
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    choice = models.CharField(max_length=2, choices=CHOICE, default=news)



    def like_post(self):
        self.rating += 1
        self.save()

    def dislike_post(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'




class PostCategory(models.Model):
    _category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post_PC = models.ForeignKey(Post, on_delete=models.CASCADE)



class Comment(models.Model):
    objects = None
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text_comment = models.TextField()
    datetime_com = models.DateTimeField(auto_now_add=True)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)



    def like_com(self):
        self.rating += 1
        self.save()


    def dislike_com(self):
        self.rating -= 1
        self.save()

