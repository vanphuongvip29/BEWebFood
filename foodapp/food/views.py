# Create your views here.
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.filters import OrderingFilter

from .serializers import (
    FoodSerializer,
    FoodDetailSerializer,
    UserSerializer,
    CategorySerializer,
    TagSerializer,
    CommentSerializer,
)
from .models import Food, FoodDetail, User, Category, Tag, Comment
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination


class AuthInfo(APIView):
    def get(self, request):
        return Response(data=settings.OAUTH2_INFO, status=status.HTTP_200_OK)


class UserViewSet(
    viewsets.ViewSet,
    generics.CreateAPIView,
    # generics.RetrieveAPIView
):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [
        MultiPartParser,
    ]

    def get_permissions(self):
        if self.action == "current_user":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=["get"], detail=False, url_path="current-user")
    def current_user(self, request):
        return Response(self.serializer_class(request.user).data)


class Pagination(PageNumberPagination):
    page_size = 6  # Số lượng mục trên mỗi trang trong ViewSet này
    page_size_query_param = "page_size"
    max_page_size = 100


class CategoryViewSet(
    viewsets.ViewSet,
    generics.ListAPIView,
    generics.CreateAPIView,
    generics.DestroyAPIView,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # pagination_class = Pagination
    # sắp xếp
    filter_backends = [OrderingFilter]
    # các trường sắp xếp
    ordering_fields = ["name"]
    # thứ tự sắp xếp asending or desending
    ordering = ["name"]


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.filter(active=True)
    serializer_class = FoodSerializer
    pagination_class = Pagination
    # sắp xếp
    filter_backends = [OrderingFilter]
    # các trường sắp xếp
    ordering_fields = ["id", "name", "created_date"]
    # thứ tự sắp xếp asending or desending
    ordering = ["id", "name", "-name", "created_date", "-created_date"]
    # Chứng thực
    # permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action == "list":
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]
    # tìm kiếm kw
    def get_queryset(self):
        # c1
        # foods = Food.objects.filter(active=True)

        # kw = self.request.query_params.get("kw")
        # if kw is not None:
        #     foods = foods.filter(name__icontains=kw)

        # cate = self.request.query_params.get("cate")
        # if cate is not None:
        #     foods = foods.filter(category__exact=cate)
        # return foods

        # c2
        query = self.queryset
        kw = self.request.query_params.get("kw")
        cate = self.request.query_params.get("cate")
        if kw is not None:
            query = query.filter(name__icontains=kw)
        if cate is not None:
            query = query.filter(category__exact=cate)

        return query

    # Lấy fooddetail of food
    @action(methods=["get"], detail=True, url_name="food-fooddetail")
    def food_fooddetail(self, request, pk):
        # try:
        f = Food.objects.get(pk=pk)
        fd = f.food_detail.filter(active=True)

        # except Food.DoesNotExist:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data=FoodDetailSerializer(fd, many=True).data,
            status=status.HTTP_200_OK,
        )

    @action(methods=["post"], detail=True, url_path="hide-food")
    def hide_food(self, request, pk):
        try:
            f = Food.objects.get(pk=pk)
            f.active = False
            f.save()
        except Food.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data=FoodSerializer(f, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )


class FoodDetailViewSet(
    viewsets.ViewSet,
    generics.ListAPIView,
    generics.CreateAPIView,
    generics.DestroyAPIView,
):
    queryset = FoodDetail.objects.filter(active=True)
    serializer_class = FoodDetailSerializer


class TagViewSet(
    viewsets.ViewSet,
    generics.ListAPIView,
    generics.CreateAPIView,
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CommentViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
