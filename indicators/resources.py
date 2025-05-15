from import_export import resources
from .models import Indicator

class IndicatorResource(resources.ModelResource):
    class Meta:
        model = Indicator
        fields = ('id', 'name', 'description', 'target', 'baseline', 'unit_of_measure')
