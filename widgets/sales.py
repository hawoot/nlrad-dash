# -*- coding: utf-8 -*-
"""Sales dashboard widget."""
import ipywidgets as widgets


def create_sales_widget():
    """Create sales dashboard with period selector and metrics."""
    metrics_html = widgets.HTML('''
        <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-top: 10px;">
            <div style="background: white; border-radius: 10px; padding: 20px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; flex: 1; min-width: 150px;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">$124.5K</div>
                <div style="color: #6c757d;">Monthly Revenue</div>
            </div>
            <div style="background: white; border-radius: 10px; padding: 20px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; flex: 1; min-width: 150px;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">1,234</div>
                <div style="color: #6c757d;">Total Orders</div>
            </div>
            <div style="background: white; border-radius: 10px; padding: 20px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; flex: 1; min-width: 150px;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">+15.3%</div>
                <div style="color: #6c757d;">Growth Rate</div>
            </div>
        </div>
    ''')

    period_selector = widgets.Dropdown(
        options=['This Month', 'Last Month', 'This Quarter', 'Last Quarter', 'This Year'],
        value='This Month',
        description='Period:'
    )
    output = widgets.Output()

    def on_period_change(change):
        with output:
            output.clear_output()
            print(f"Loading data for: {change['new']}")

    period_selector.observe(on_period_change, names='value')
    return widgets.VBox([period_selector, metrics_html, output])
