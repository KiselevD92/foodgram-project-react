from django.urls import include, path
from rest_framework import routers

from api.v1.views import RecipeViewSet, TagViewSet, IngredientViewSet, UsersViewSet, FollowViewSet

v1_router = routers.DefaultRouter()
v1_router.register('recipes', RecipeViewSet, basename='recipes')
# v1_router.register(r'recipes/download_shopping_cart', DownloadCartViewSet, basename='download')
# v1_router.register(r'recipes/(?P<recipes_id>\d+)/shopping_cart', ShoppingViewSet, basename='shopping')
# v1_router.register(r'recipes/(?P<recipes_id>\d+)/favorite', FavoriteViewSet, basename='favorite')
v1_router.register('tags', TagViewSet, basename='tags')
v1_router.register('ingredients', IngredientViewSet, basename='ingredients')
v1_router.register(r'users/(?P<users_id>\d+)/subscribe/', FollowViewSet, basename='subscribe')
v1_router.register(r'users', UsersViewSet, basename='users')
# v1_router.register(r'users/(?P<id>\d+)/subscribe/', FollowViewSet, basename='subscribe')




urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
