from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Food, Tag, FoodDetail, User, Category
from rest_framework import serializers


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class FoodDetailSerializer(ModelSerializer):
    # many = True vì có nhiều object
    tags = TagSerializer(many=True)

    image_path = SerializerMethodField()

    def get_image_path(self, img):

        name = img.image.name
        if name.startswith("static/"):
            path = "http://127.0.0.1:8000/%s" % name

        else:
            path = "http://127.0.0.1:8000/static/%s" % name

        return path

    class Meta:
        model = FoodDetail
        fields = ["id", "name", "content", "created_date", "food", "image_path", "tags"]


class FoodSerializer(ModelSerializer):
    food_detail = FoodDetailSerializer(many=True)
    image_path = serializers.SerializerMethodField(source="image")

    def get_image_path(self, obj):
        request = self.context.get("request")
        path = "/static/%s" % obj.image.name
        if request:
            return request.build_absolute_uri(path)

    class Meta:
        model = Food
        fields = [
            "id",
            "name",
            "description",
            "created_date",
            "category",
            "image_path",
            "active",
            "food_detail",
        ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "avatar",
        ]
        extra_kwargs = {"password": {"write_only": "True"}}

    # mã hóa password
    def create(self, validated_data):
        u = User(**validated_data)
        u.set_password(validated_data["password"])
        u.save()
        return u
