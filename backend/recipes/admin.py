from django.contrib import admin

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient
from users.models import User


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    search_fields = ('name', 'author',)
    list_filter = ('author', 'name', 'tag',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username',)
    search_fields = ('email', 'username',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(User, UserAdmin)
