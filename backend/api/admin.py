from django.contrib import admin
from .models import FoodItem, Category

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price')   # Removed duplicate 'category'
    search_fields = ('name', 'category')


from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
