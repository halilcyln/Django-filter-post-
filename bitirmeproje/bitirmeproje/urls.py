from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indexPage, name='indexPage'),
    path('iletisim/', contactPage, name='contactPage'),
    path('detail/<slug>/<category>', detailPage ,name='detailPage'),
    path('<str:category>', categoryPage ,name='categoryPage'),
    path('login/', loginPage, name='loginPage'),
    path('register/', registerPage, name='registerPage'),
    path('logout/', logoutPage, name='logout'),
    path('favori/<user>/', favoriPage, name='favoriPage'),
    path('api', favoriPage, name='favoriPage'),
         
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
