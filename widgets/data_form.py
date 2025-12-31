# -*- coding: utf-8 -*-
"""Data entry form widget."""
import ipywidgets as widgets


def create_data_form_widget():
    """Create data entry form with submit/clear buttons."""
    name_input = widgets.Text(description='Name:', placeholder='Enter name')
    email_input = widgets.Text(description='Email:', placeholder='Enter email')
    category_select = widgets.Dropdown(
        options=['Category A', 'Category B', 'Category C'],
        description='Category:'
    )
    priority_select = widgets.RadioButtons(
        options=['Low', 'Medium', 'High'],
        description='Priority:'
    )
    notes_input = widgets.Textarea(
        description='Notes:',
        placeholder='Additional notes...',
        layout=widgets.Layout(width='400px', height='100px')
    )

    submit_btn = widgets.Button(
        description='Submit',
        button_style='success',
        icon='check'
    )
    clear_btn = widgets.Button(
        description='Clear',
        button_style='warning',
        icon='eraser'
    )
    output = widgets.Output()

    def on_submit(b):
        with output:
            output.clear_output()
            print(f"Submitted: {name_input.value}, {email_input.value}")
            print(f"Category: {category_select.value}, Priority: {priority_select.value}")

    def on_clear(b):
        name_input.value = ''
        email_input.value = ''
        notes_input.value = ''
        with output:
            output.clear_output()

    submit_btn.on_click(on_submit)
    clear_btn.on_click(on_clear)

    return widgets.VBox([
        name_input,
        email_input,
        category_select,
        priority_select,
        notes_input,
        widgets.HBox([submit_btn, clear_btn]),
        output
    ])
