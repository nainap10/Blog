from django.contrib import admin
from .models import Product, Blog
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('price',)
    ordering = ('price',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'image')
    search_fields = ('title',)
    ordering = ('created_at',)