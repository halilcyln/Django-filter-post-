from django.shortcuts import render, redirect
from myapp.models import *
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
def categoryPage(request, category):
    filter = Cards.objects.filter(category=category)
    context={
        "filter":filter,
    }
    return render(request,'category.html',context)



def contactPage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        emailmessage = request.POST.get("emailmessage")

        # Kullanıcının gönderdiği mesaj ve email adresini kendi email adresinize gönder
        send_mail(
            'Yeni İletişim Formu Mesajı',
            f'Email: {email}\nMesaj: {emailmessage}',
            'halillcyln5@gmail.com',  # Gönderen email adresi, kendi email adresiniz olabilir
            ['halillcyln5@gmail.com'],  # Alıcı email adresi, kendi email adresiniz olabilir
            fail_silently=False,
        )

        messages.success(request, "Mesajınız iletildi")

    return render(request, 'contact.html',)


def indexPage(request):
    cards_tel = Cards.objects.filter(category="Film")
    cards_pc = Cards.objects.filter(category="Dizi")
    cards_tablet = Cards.objects.filter(category="Belgesel")
    cards_random = Cards.objects.all().order_by('?')[:5] 
    context = {
        "cards_random":cards_random,
        "cards_tel": cards_tel,
        "cards_pc": cards_pc,
        "cards_tablet": cards_tablet,
    }
    return render(request,'index.html',context)

def detailPage(request, slug, category):
    cards = get_object_or_404(Cards, slug=slug, category=category)
    card = Cards.objects.filter(slug=slug, category=category)
    yorum = Yorum.objects.filter(card__slug=slug)

    if request.method == "POST":
        if "user_favori" in request.POST:
            # Kullanıcının bu kartı daha önce favoriye ekleyip eklemediğini kontrol et
            favori_kontrol = Favori.objects.filter(user=request.user, product=cards).exists()

            if favori_kontrol:
                messages.warning(request, 'Bu kart zaten favorilerinizde bulunmaktadır.')
            else:
                # Kartı favorilere ekle
                Favori.objects.create(user=request.user, product=cards)
                messages.success(request, 'Kart favorilere eklendi')

        elif "yorum_submit" in request.POST:
            text = request.POST.get("yorum")
            yorum_user = request.POST.get("yorum_user")

            if text.strip() and yorum_user:
                Yorum.objects.create(card=cards, text=text, user=yorum_user)
                messages.success(request, 'Yorumunuz paylaşıldı')
            else:
                messages.error(request, 'Yorum alanı boş kullanılmaz')

    context = {
        "cards": cards,
        "card": card,
        "yorum": yorum
    }
    return render(request, 'detail.html', context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        login(request, user)
        messages.success(request,'Giriş yaptınız')
        return redirect("indexPage")
    else:
        messages.error(request,"Kullanıcı adı veya şifre hatalı")
        
    context={}
    return render(request, 'user/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('indexPage')

def registerPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        if password == password1:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=username, email=email, password=password)
                    login(request, user)
                    messages.success(request, 'Üye kaydınız başarıyla oluşturuldu.')
                    return redirect("indexPage")
                else:
                    messages.error(request, 'Bu e-posta adresi zaten kullanımda.')
            else:
                messages.error(request, 'Bu kullanıcı adı zaten alınmış.')
        else:
            messages.error(request, 'Şifreler eşleşmiyor.')

    return render(request, 'user/register.html')


def favoriPage(request, user):
    user_filter = Favori.objects.filter(user=request.user)
    context = {
        "user_filter":user_filter,
        "current_user": request.user,
    }
    return render(request,'favori.html',context)


 

        

