from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import RecipeFilterSet, IngredientSearchFilter
from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag
from .pagination import LimitPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (ImageRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_class = RecipeFilterSet
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return self.queryset.add_user_annotations(user_id=self.request.user)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        if request.method == "POST":
            return self.add_obj(Favorite, request.user, pk)
        elif request.method == "DELETE":
            return self.delete_obj(Favorite, request.user, pk)
        return None

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        if request.method == "POST":
            return self.add_obj(Cart, request.user, pk)
        elif request.method == "DELETE":
            return self.delete_obj(Cart, request.user, pk)
        return None

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__purchases__user=request.user
        )
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in shopping_list:
                shopping_list[name] = {
                    "measurement_unit": measurement_unit,
                    "amount": amount,
                }
            else:
                shopping_list[name]["amount"] += amount
        main_list = [
            f"* {item}:{value['amount']}" f"{value['measurement_unit']}\n"
            for item, value in shopping_list.items()
        ]
        response = HttpResponse(main_list, "Content-Type: text/plain")
        response["Content-Disposition"] = 'attachment; filename="BuyList.txt"'
        return response

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {"errors": "Рецепт уже добавлен в список"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ImageRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Рецепт уже удален"}, status=status.HTTP_400_BAD_REQUEST
        )


class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ("^name",)