# -*- coding: utf-8 -*-
"""UI construction functions for the dashboard."""
from typing import List
import ipywidgets as widgets

from models import GroupConfig
from widgets.registry import WIDGET_REGISTRY


def build_group_ui(group: GroupConfig, level: int = 0) -> widgets.Widget:
    """Build UI for a group and its contents."""
    children = []

    # Add widgets in this group
    for widget_config in group.widgets:
        if widget_config.id in WIDGET_REGISTRY:
            widget_ui = WIDGET_REGISTRY[widget_config.id]()
            widget_box = widgets.VBox([
                widgets.HTML(
                    f'<h4 style="margin: 0 0 10px 0;">{widget_config.name}</h4>'
                ),
                widgets.HTML(
                    f'<p style="color: #666; margin: 0 0 15px 0;">'
                    f'{widget_config.description}</p>'
                ),
                widget_ui
            ])
            children.append((widget_config.name, widget_box))

    # Add nested groups
    for subgroup in group.groups:
        subgroup_ui = build_group_ui(subgroup, level + 1)
        children.append((subgroup.name, subgroup_ui))

    # If only one child, return it directly
    if len(children) == 1:
        return children[0][1]

    # Multiple children - use accordion
    if children:
        accordion = widgets.Accordion(children=[c[1] for c in children])
        for i, (name, _) in enumerate(children):
            accordion.set_title(i, name)
        return accordion

    return widgets.HTML('<p>No content available</p>')


def build_dashboard_ui(
    title: str, groups: List[GroupConfig], username: str
) -> widgets.Widget:
    """Build the complete dashboard UI from filtered groups."""
    if not groups:
        return widgets.HTML(f'''
            <div style="text-align: center; padding: 40px;">
                <h3>Welcome, {username}</h3>
                <p style="color: #666;">No widgets available for your access level.</p>
            </div>
        ''')

    # Build tabs for top-level groups
    tab_children = []
    tab_titles = []

    for group in groups:
        group_ui = build_group_ui(group)
        tab_children.append(group_ui)
        tab_titles.append(group.name)

    tabs = widgets.Tab(children=tab_children)
    for i, title_text in enumerate(tab_titles):
        tabs.set_title(i, title_text)

    # Header
    header = widgets.HTML(f'''
        <div style="display: flex; justify-content: space-between; align-items: center;
                    padding: 10px 0; margin-bottom: 15px; border-bottom: 2px solid #667eea;">
            <h2 style="margin: 0; color: #333;">{title}</h2>
            <span style="background: #667eea; color: white; padding: 5px 15px;
                         border-radius: 20px; font-size: 0.9rem;">User: {username}</span>
        </div>
    ''')

    return widgets.VBox([header, tabs])
