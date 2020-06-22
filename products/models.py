from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Feedback(models.Model):
    verified = models.BooleanField('Отправить ответ на e-mail')
    email_adress = models.CharField('e-mail адрес для ответа', blank=True, max_length=500)
    email_reply_capt = models.CharField('Заголовок ответа на e-mail', blank=True, max_length=500)
    email_reply_text = models.TextField('Текст ответа на e-mail', null=True, blank=True)


class Category(models.Model):
    # категория
    name = models.CharField("Категория", max_length=100)
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Manufacturer(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="manufacturer/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class CPU(models.Model):
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="cpu_image/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Процессор"
        verbose_name = "Процессоры"


class Product(models.Model):
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    year = models.PositiveSmallIntegerField("Дата выхода на рынок", default=2010, null=True)
    manufact = models.ManyToManyField(Manufacturer, verbose_name="производитель", related_name="prod_manuf")
    screen_diagonal = models.PositiveSmallIntegerField("Диагональ экрана", default=6.0)
    battery = models.PositiveSmallIntegerField("Ёмкость аккумулятора", default=2000, help_text="указывать в mAh ")
    price = models.PositiveSmallIntegerField("Цена", default=0)
    image = models.ImageField("Изображение", upload_to="product/")
    cpus = models.ManyToManyField(CPU, verbose_name="процессор", related_name="prod_cpu")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=150, unique=True)
    favourite = models.ManyToManyField(User, related_name="favourite", blank=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name_plural = "Продукты"
        verbose_name = "Продукт"


class ProductImage(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="prod_image/")
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звёзды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField("IP", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="продукт")

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=1000)
    product = models.ForeignKey(Product, verbose_name="продукт", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name_plural = "Отзывы"
        verbose_name = "Отзыв"
