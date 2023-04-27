from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    autoUser = models.OneToOneField(User, on_delete= models.CASCADE)
    rating  = models.IntegerField(default = 0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating = Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commRat = self.autoUser.comment_set.aggregate(commRating = Sum('comm_rating'))
        cRat = 0
        cRat += commRat.get('commRating')

        self.rating = pRat * 3 + cRat
        self.save()



class Category(models.Model):
    name = models.CharField(max_length = 64, unique= True, verbose_name='Категория')

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOISE = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length= 2, choices= CATEGORY_CHOISE, default= ARTICLE, verbose_name='Тип')

    dateCreate = models.DateTimeField(auto_now_add = True)
    postCategory = models.ManyToManyField(Category, through= 'PostCategory', verbose_name='Категория')
    title = models.CharField(max_length = 256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Содержимое')
    rating  = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    # def __str__(self):
    #     pass


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)


class Comment(models.Model):
    comm_post = models.ForeignKey(Post, on_delete = models.CASCADE)
    comm_user = models.ForeignKey(User, on_delete = models.CASCADE)
    comm_text = models.TextField()
    date_create = models.DateTimeField(auto_now_add = True)
    comm_rating = models.IntegerField(default = 0)

    def like(self):
        self.comm_rating += 1
        self.save()

    def dislike(self):
        self.comm_rating -= 1
        self.save()