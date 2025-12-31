# -*- coding: utf-8 -*-
"""Widget registry - maps widget IDs to their creation functions."""
from widgets.sales import create_sales_widget
from widgets.metrics import create_metrics_widget
from widgets.data_form import create_data_form_widget
from widgets.settings import create_settings_widget

WIDGET_REGISTRY = {
    "sales_dashboard": create_sales_widget,
    "metrics": create_metrics_widget,
    "data_form": create_data_form_widget,
    "settings": create_settings_widget,
}
