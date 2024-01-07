from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.


class Cards(models.Model):
    CHOİCES = (
        ("Film", "Film"),
        ("Dizi", "Dizi"),
        ("Belgesel", "Belgesel"),
    )
    image = models.ImageField(("Kart resmi ekleyin"), upload_to='images', max_length=300)
    brand = models.CharField(("Marka Ekleyin"), max_length=50)
    category = models.CharField(("Kategori ekleyin Ekleyin"),choices=CHOİCES, max_length=50)
    title = models.CharField(("Ürün başlığı ekleyin"), max_length=50)
    slug = models.SlugField(("Slug"), null=True, blank=True)
    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()
    
    def __str__(self):
        return self.title
    
class Yorum(models.Model):
    user = models.CharField(("Kullanıcı"), max_length=50, null=True)
    card = models.ForeignKey(Cards, verbose_name=("Ürün adı"), on_delete=models.CASCADE, null=True)
    text = models.TextField(("Yorum"))
    
    
class Register(models.Model):
    name = models.CharField(("Kullanıcı adı"), max_length=50)
    password = models.CharField(("Parola"), max_length=50)
    email = models.EmailField(("Email adresi"), max_length=254)
    
    def __str__(self):
        return self.name
    
    
class Favori(models.Model):
    user = models.ForeignKey(User, verbose_name=("Favoriye ekleyen kullanıcı"), on_delete=models.CASCADE)
    product = models.ForeignKey(Cards, verbose_name=("Kart Adı"), on_delete=models.CASCADE)
    
    