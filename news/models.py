from django.db import models
from django.contrib.auth.models import User




class Author(models.Model):
    rating_author = models.IntegerField(default=0)
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        rating_Post = Post.objects.filter(autor_post=self).values('rating_post')
        rating_Post = sum(p['rating_post'] for p in rating_Post) * 3

        rating_Comment = Comment.objects.filter(comment_user=self.author).values('rating_comment')
        rating_Comment = sum(c['rating_comment'] for c in rating_Comment)

        com_aut_rat = Post.objects.filter(author_post=self).values('comment_post__rating_comment')
        com_aut_rat = sum(c['comment_post__rating_comment'] for c in com_aut_rat)

        rating_author = rating_Post + rating_Comment + com_aut_rat

        self.rating_author = rating_author
        self.save()

        return f'{self.rating_author}'


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
    rating_post = models.IntegerField(default=0)
    datetime_post = models.DateTimeField(auto_now_add=True)
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    choice = models.CharField(max_length=2, choices=CHOICE, default=news)



    def like_post(self):
        self.rating_post += 1
        self.save()

    def dislike_post(self):
        self.rating_post -= 1
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
    rating_comment = models.IntegerField(default=0)



    def like_com(self):
        self.rating_comment += 1
        self.save()


    def dislike_com(self):
        self.rating_comment -= 1
        self.save()

