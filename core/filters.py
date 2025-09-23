import django_filters
from .models import Category

class CategoryFilter(django_filters.FilterSet):
    # Rename parameter "parent" instead of "parent_category__category_slug"
    parent = django_filters.CharFilter(
        field_name="parent_category__category_slug", lookup_expr="exact"
    )
    status = django_filters.BooleanFilter(
        field_name="status", lookup_expr="exact"
    )

    class Meta:
        model = Category
        fields = ["parent", "status"]