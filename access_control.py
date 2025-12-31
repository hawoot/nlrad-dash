# -*- coding: utf-8 -*-
"""Access control for dashboard widgets."""
from typing import Set, Optional, List

from models import DashboardConfig, WidgetConfig, GroupConfig


class AccessController:
    """Controls access to widgets based on user permissions."""

    def __init__(self, config: DashboardConfig):
        self.config = config
        self._permission_cache: dict = {}

    def get_user_permissions(self, username: str) -> Set[str]:
        """Get all permissions for a user."""
        if username in self._permission_cache:
            return self._permission_cache[username]

        permissions: Set[str] = set()
        ac = self.config.access_control

        # Add default permissions
        permissions.update(ac.default_permissions)

        # Add user-specific permissions
        if username in ac.users:
            user_config = ac.users[username]

            # Add permissions from roles
            for role_name in user_config.roles:
                if role_name in ac.roles:
                    permissions.update(ac.roles[role_name].permissions)

            # Add additional direct permissions
            permissions.update(user_config.additional_permissions)

        self._permission_cache[username] = permissions
        return permissions

    def can_access_widget(self, widget: WidgetConfig, username: str) -> bool:
        """Check if user can access a specific widget."""
        user_permissions = self.get_user_permissions(username)
        required = set(widget.permissions)

        # If no permissions required, widget is accessible to all
        if not required:
            return True

        return required.issubset(user_permissions)

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

    def clear_cache(self):
        """Clear the permission cache."""
        self._permission_cache.clear()
