from django.db import models
from werkzeug.security import generate_password_hash,check_password_hash
# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=24)
    password_hash = models.CharField(max_length=128)
    email = models.EmailField()

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    # 设置password_hash
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    # 验证password
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __str__(self):
        return self.username


class Commod(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    image = models.CharField(max_length=64)
    price = models.IntegerField()
    types = models.CharField(max_length=32)


    def __str__(self):
        return self.title


class Detail(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    recipient = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    postcode = models.IntegerField()
    phone = models.IntegerField()


    def __str__(self):
        return self.recipient

class Cat(models.Model):
    id = models.AutoField(primary_key=True)
    commod = models.ForeignKey(Commod, on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    images = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    price = models.IntegerField()
    num = models.IntegerField()
    price_all = models.IntegerField()
    def __str__(self):
        return self.title

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    commod = models.ForeignKey(Cat, null=True, on_delete=models.SET_NULL)
    times = models.DateTimeField()
    order = models.IntegerField()
    images = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    types = models.BooleanField()
    num = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.title
