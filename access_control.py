# -*- coding: utf-8 -*-
"""Access control for dashboard widgets."""
from typing import Set, Optional, List

from models import DashboardConfig, WidgetConfig, GroupConfig, UserConfig


class AccessController:
    """Controls access to widgets based on user roles."""

    def __init__(self, config: DashboardConfig):
        self.config = config

    def get_user_roles(self, username: str) -> Set[str]:
        """Get all roles for a user."""
        user_config = self.config.access_control.users.get(username, UserConfig())
        return set(user_config.roles)

    def can_access_widget(self, widget: WidgetConfig, username: str) -> bool:
        """Check if user can access a specific widget."""
        user_roles = self.get_user_roles(username)
        widget_roles = set(widget.roles)

        # If no roles specified, widget is accessible to all
        if not widget_roles:
            return True

        # User can access if they have ANY matching role
        return bool(user_roles & widget_roles)

    def filter_groups_for_user(
        self, username: str, groups: Optional[List[GroupConfig]] = None
    ) -> List[GroupConfig]:
        """Filter group hierarchy to only show accessible items."""
        if groups is None:
            groups = self.config.groups

        filtered = []
        for group in groups:
            filtered_group = self._filter_group(group, username)
            if filtered_group is not None:
                filtered.append(filtered_group)
        return filtered

    def _filter_group(
        self, group: GroupConfig, username: str
    ) -> Optional[GroupConfig]:
        """Recursively filter a group and its children."""
        # Filter nested groups recursively
        filtered_subgroups = self.filter_groups_for_user(username, group.groups)

        # Filter widgets
        filtered_widgets = [
            w for w in group.widgets if self.can_access_widget(w, username)
        ]

        # Only include group if it has accessible content
        if filtered_subgroups or filtered_widgets:
            return GroupConfig(
                id=group.id,
                name=group.name,
                description=group.description,
                icon=group.icon,
                groups=filtered_subgroups,
                widgets=filtered_widgets,
            )
        return None
