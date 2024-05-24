from django.contrib import admin
from django.contrib.auth.models import Permission
from django.urls.resolvers import URLResolver
from .models import Category, Food, FoodDetail, Tag, User
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from django.template.response import TemplateResponse


class FoodDetailForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = FoodDetail
        fields = "__all__"


class FoodDetailTagInline(admin.StackedInline):
    model = FoodDetail.tags.through


class FoodDetailAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "active", "food"]
    search_fields = ["name", "created_date", "food__name"]
    list_filter = ["name", "food__name"]

    readonly_fields = ["avatar"]

    form = FoodDetailForm

    inlines = (FoodDetailTagInline,)

    def avatar(self, foodDetail):
        return mark_safe(
            '<img src="/static/{url}" alt="{alt}" width="120"/>'.format(
                url=foodDetail.image.name, alt=foodDetail.name
            )
        )


class FoodDetailInline(admin.StackedInline):
    model = FoodDetail
    pk_name = "food"


class FoodAdmin(admin.ModelAdmin):
    inlines = (FoodDetailInline,)


class FoodAppAdminSite(admin.AdminSite):
    site_header = "Hệ thống quản lý Food"

    def get_urls(self):
        return [path("food-stats/", self.food_stats)] + super().get_urls()

    # stats
    def food_stats(self, request):
        food_count = Food.objects.count()

        return TemplateResponse(
            request, "admin/food-stats.html", {"food_count": food_count}
        )


admin_site = FoodAppAdminSite(name="myadmin")


# Register your models here.

admin.site.register(Category)
admin.site.register(Food, FoodAdmin)
admin.site.register(FoodDetail, FoodDetailAdmin)
admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Permission)

# admin_site.register(Category)
# admin_site.register(Food, FoodAdmin)
# admin_site.register(FoodDetail, FoodDetailAdmin)
# admin_site.register(Tag)
