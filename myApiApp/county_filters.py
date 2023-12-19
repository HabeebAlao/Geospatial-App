from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis.filters import GeometryFilter
from django_filters import filters
from .models import eds, counties


class CountyElectoralFilter(GeoFilterSet):
    constituency = filters.CharFilter(method='get_electorals_by_county')

    class Meta:
        model = counties

        exclude = ['geom']

    def get_electorals_by_county(self, queryset, name, value):
        query_ = eds.objects.filter(pk=value)

        if query_:
            obj = query_.first()

            return queryset.filter(geom__within=obj.geom)

        return queryset