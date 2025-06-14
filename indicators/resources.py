from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Indicator, IndicatorCategory
from logframe.models import Output

class IndicatorResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(IndicatorCategory, 'name')
    )
    output = fields.Field(
        column_name='output',
        attribute='output',
        widget=ForeignKeyWidget(Output, 'title')
    )

    class Meta:
        model = Indicator
        fields = (
            'id', 'name', 'description', 'category', 'output',
            'baseline', 'target', 'actual', 'unit',
            'created_at', 'updated_at'
        )
        export_order = fields
