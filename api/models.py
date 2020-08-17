from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '<%s>' % self.title

    class Meta:
        db_table = 'old_boy_book'
        verbose_name = '书籍'
        verbose_name_plural = verbose_name

class User(models.Model):
    SEX_CHOICES = [
        [0, '男'],
        [1, '女']
    ]
    name = models.CharField(max_length=64)
    pwd = models.CharField(max_length=32)
    phone = models.CharField(max_length=11, default='', blank=True)
    sex = models.IntegerField(choices=SEX_CHOICES, default=0)
    icon = models.ImageField(upload_to='icon', default='icon/default.jpg')

    def __str__(self):
        return '<%s>' % self.name

    class Meta:
        db_table = 'old_boy_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

"""
book表：name、price、img、authors、publish、is_delete、create_time
publish表：name、address、is_delete、create_time
Author表：name、age、is_delete、create_time
AuthorDetail表：mobile、author、is_delete、create_time
"""

class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Books(BaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(upload_to='icon', default='icon/default.jpg')
    publish = models.ForeignKey(to='Publish', on_delete=models.CASCADE)
    authors = models.ManyToManyField('Author')

    @property
    def publish_name(self):
        return self.publish.name

    @property
    def author_list(self):
        return self.authors.values('name', 'age', 'authordetail__mobile')

    class Meta:
        db_table = 'books'
        verbose_name = '书'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Publish(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    class Meta:
        db_table = 'publish'
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Author(BaseModel):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    class Meta:
        db_table = 'authors'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class AuthorDetail(BaseModel):
    mobile = models.CharField(max_length=11)
    author = models.OneToOneField(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'author_detail'
        verbose_name = '作者详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}的详情'.format(self.author.name)

#


















