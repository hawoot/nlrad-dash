# -*- coding: utf-8 -*-
"""Dashboard application entry point."""
from config import get_config
from access_control import AccessController
from ui_builder import build_dashboard_ui


def create_app(username: str = "alice"):
    """
    Create and return the dashboard application widget.

    Args:
        username: The username to load the dashboard for.
                  Different users see different widgets based on their role.

    Returns:
        An ipywidgets widget containing the dashboard.
    """
    config = get_config()
    ac = AccessController(config)
    filtered_groups = ac.filter_groups_for_user(username)
    return build_dashboard_ui(config.title, filtered_groups, username)
