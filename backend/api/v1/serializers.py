from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import serializers

from recipes.models import (
    Recipe, Tag,
    Ingredient, Favorite,
    ShoppingCart, RecipeIngredient
)
from users.models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        if Follow.objects.filter(
                user=self.context['request'].user, following=obj
        ).exists():
            return True
        return False


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})
    current_password = serializers.CharField(style={"input_type": "password"})

    def validate(self, obj):
        try:
            validate_password(obj["new_password"])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )
        return super().validate(obj)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=True)
    tag = TagSerializer(required=True)
    ingredients = RecipeIngredientSerializer(
        many=True, required=True, source='recipes'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tag',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        if Favorite.objects.filter(
                user=self.context['request'].user, recipe=obj
        ).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        if ShoppingCart.objects.filter(
                user=self.context['request'].user, recipe=obj
        ).exists():
            return True
        return False


class ShortInfoRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        if Follow.objects.filter(
                user=self.context['request'].user, following=obj
        ).exists():
            return True
        return False

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        serializer = ShortInfoRecipeSerializer(
            recipes, many=True, read_only=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
