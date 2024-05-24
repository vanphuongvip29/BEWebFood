from django.urls import path, include
from . import views
from rest_framework import routers

# admin
from food.admin import admin_site

routers = routers.DefaultRouter()
routers.register("foods", views.FoodViewSet)
routers.register("fooddetails", views.FoodDetailViewSet)
routers.register("users", views.UserViewSet)
routers.register("categorys", views.CategoryViewSet, basename="category")
routers.register("tags", views.TagViewSet, basename="tag")


urlpatterns = [
    path("", include(routers.urls)),
    path("oauth2_info/", views.AuthInfo.as_view(), name="oauth2-info"),
    #
    # biểu thức chính quy
    # re_path(r"^welcome2/(?P<year2>[0-9]{1,2})/$", views.welcome2),
    #
    # path("admin/", admin_site.urls),
]
