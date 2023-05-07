from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.v1.permissions import IsAuthorOrReadOnly
from api.v1.serializers import (
    RecipeSerializer, TagSerializer,
    IngredientSerializer, UserSerializer,
    FollowSerializer, ShortInfoRecipeSerializer,
    SetPasswordSerializer
)
from recipes.models import Recipe, Tag, Ingredient, Favorite, ShoppingCart
from users.models import User, Follow


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = ShortInfoRecipeSerializer(recipe, data=request.data)
            serializer.is_valid(raise_exception=True)
            if ShoppingCart.objects.filter(
                    user=request.user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в корзину'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(
                ShoppingCart, user=request.user, recipe=recipe
            ).delete()
            return Response(
                {'detail': 'Удаление из корзины прошло успешно'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        result = ShoppingCart.object.get(user=self.request.user)
        response = HttpResponse(
            'Список покупок: ' + result,
            content_type='text/plain'
        )
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_cart.txt"'
        return response

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = ShortInfoRecipeSerializer(recipe, data=request.data)
            serializer.is_valid(raise_exception=True)
            if Favorite.objects.filter(
                    user=request.user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorite.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(
                Favorite, user=request.user, recipe=recipe
            ).delete()
            return Response(
                {'detail': 'Удаление из избранного прошло успешно'},
                status=status.HTTP_204_NO_CONTENT
            )


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)


class CustomUsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['post'])
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()
        return Response(
            {'detail': 'Пароль успешно изменен'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['get'])
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        serializer = FollowSerializer(
            queryset, many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=(IsAuthenticated,),
            methods=['post', 'delete'])
    def subscribe(self, request, **kwargs):
        following = get_object_or_404(User, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = FollowSerializer(
                following, data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            if Follow.objects.filter(
                    user=request.user,
                    following=following
            ).exists():
                return Response(
                    {'errors': 'Подписка уже активна'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Follow.objects.create(user=request.user, following=following)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(
                Follow, user=request.user, following=following
            ).delete()
            return Response(
                {'detail': 'Подписка успешно отменена'},
                status=status.HTTP_204_NO_CONTENT
            )
