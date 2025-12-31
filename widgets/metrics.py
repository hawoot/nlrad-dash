# -*- coding: utf-8 -*-
"""System metrics widget."""
import datetime
import ipywidgets as widgets


def create_metrics_widget():
    """Create system metrics display with refresh button."""
    metrics_html = widgets.HTML('''
        <div style="max-width: 600px; margin-top: 10px;">
            <div style="background: white; border-radius: 10px; padding: 20px; margin-bottom: 15px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <strong>CPU Usage</strong>
                <div style="background: #e9ecef; border-radius: 5px; height: 25px; margin-top: 10px;">
                    <div style="background: #28a745; width: 45%; height: 100%; border-radius: 5px;
                                text-align: center; color: white; line-height: 25px;">45%</div>
                </div>
            </div>
            <div style="background: white; border-radius: 10px; padding: 20px; margin-bottom: 15px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <strong>Memory Usage</strong>
                <div style="background: #e9ecef; border-radius: 5px; height: 25px; margin-top: 10px;">
                    <div style="background: #ffc107; width: 72%; height: 100%; border-radius: 5px;
                                text-align: center; color: black; line-height: 25px;">72%</div>
                </div>
            </div>
            <div style="background: white; border-radius: 10px; padding: 20px; margin-bottom: 15px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <strong>Disk Usage</strong>
                <div style="background: #e9ecef; border-radius: 5px; height: 25px; margin-top: 10px;">
                    <div style="background: #17a2b8; width: 58%; height: 100%; border-radius: 5px;
                                text-align: center; color: white; line-height: 25px;">58%</div>
                </div>
            </div>
        </div>
    ''')

    refresh_btn = widgets.Button(
        description='Refresh Metrics',
        button_style='primary',
        icon='sync'
    )
    status_label = widgets.Label(value='Last updated: Just now')

    def on_refresh(b):
        status_label.value = f'Last updated: {datetime.datetime.now().strftime("%H:%M:%S")}'

    refresh_btn.on_click(on_refresh)
    return widgets.VBox([widgets.HBox([refresh_btn, status_label]), metrics_html])
