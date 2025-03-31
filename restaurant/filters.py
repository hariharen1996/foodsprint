from django_filters import FilterSet
import django_filters
from .models import FoodItems

class FoodItemFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name',lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price',lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price',lookup_expr='lte')
    food_type = django_filters.ChoiceFilter(choices=FoodItems.FOOD_CHOICES)

    class Meta:
        model = FoodItems
        fields = ['name','category','min_price','max_price','food_type']    
    