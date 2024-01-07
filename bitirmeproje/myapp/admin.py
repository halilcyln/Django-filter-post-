from django.contrib import admin
from myapp.models import *
# Register your models here.
# admin.site.register(Cards)


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    '''Admin View for Cards'''

    list_display = ('title','brand','category',)
    search_fields = ('title','brand','category',)
    
admin.site.register(Yorum)
admin.site.register(Register)
admin.site.register(Favori)