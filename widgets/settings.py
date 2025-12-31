# -*- coding: utf-8 -*-
"""Settings widget."""
import ipywidgets as widgets


def create_settings_widget():
    """Create settings panel with display and notification options."""
    # Display settings
    theme_select = widgets.Dropdown(
        options=['Light', 'Dark', 'Auto'],
        value='Light',
        description='Theme:'
    )
    cards_per_row = widgets.IntSlider(
        value=3,
        min=2,
        max=4,
        description='Cards/row:'
    )
    show_descriptions = widgets.Checkbox(
        value=True,
        description='Show widget descriptions'
    )

    # Notification settings
    email_notifications = widgets.Checkbox(
        value=True,
        description='Email notifications'
    )
    notification_frequency = widgets.Dropdown(
        options=['Immediately', 'Hourly', 'Daily', 'Weekly'],
        value='Daily',
        description='Frequency:'
    )

    save_btn = widgets.Button(
        description='Save Settings',
        button_style='success',
        icon='save'
    )
    output = widgets.Output()

    def on_save(b):
        with output:
            output.clear_output()
            print("Settings saved successfully!")

    save_btn.on_click(on_save)

    display_section = widgets.VBox([
        widgets.HTML('<h4 style="margin: 0 0 10px 0;">Display Settings</h4>'),
        theme_select,
        cards_per_row,
        show_descriptions
    ])
    notification_section = widgets.VBox([
        widgets.HTML('<h4 style="margin: 15px 0 10px 0;">Notifications</h4>'),
        email_notifications,
        notification_frequency
    ])

    return widgets.VBox([display_section, notification_section, save_btn, output])
