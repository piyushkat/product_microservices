from django.contrib import admin
from product.models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display= ('id','user','name','created_at','updated_at')
admin.site.register(Category,CategoryAdmin)
