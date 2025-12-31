# -*- coding: utf-8 -*-
"""Dashboard configuration."""
from models import (
    DashboardConfig,
    GroupConfig,
    WidgetConfig,
    AccessControlConfig,
    RoleConfig,
    UserConfig,
)


def get_config() -> DashboardConfig:
    """Return the dashboard configuration."""
    return DashboardConfig(
        version="1.0",
        title="NLRAD Dashboard",
        description="Enterprise Analytics & Management Dashboard",
        groups=[
            GroupConfig(
                id="analytics",
                name="Analytics",
                description="Data analysis and reporting tools",
                icon="chart-bar",
                groups=[
                    GroupConfig(
                        id="analytics.performance",
                        name="Performance",
                        description="System and application performance metrics",
                        icon="tachometer-alt",
                        widgets=[
                            WidgetConfig(
                                id="metrics",
                                name="System Metrics",
                                description="Real-time system health and performance metrics",
                                icon="heartbeat",
                                permissions=["analytics.view", "analytics.performance"],
                            )
                        ],
                    )
                ],
                widgets=[
                    WidgetConfig(
                        id="sales_dashboard",
                        name="Sales Dashboard",
                        description="Monthly and quarterly sales overview",
                        icon="dollar-sign",
                        permissions=["analytics.view"],
                    )
                ],
            ),
            GroupConfig(
                id="data_entry",
                name="Data Entry",
                description="Data input and management tools",
                icon="edit",
                widgets=[
                    WidgetConfig(
                        id="data_form",
                        name="Data Entry Form",
                        description="Standard data input forms",
                        icon="clipboard-list",
                        permissions=["data_entry.edit"],
                    )
                ],
            ),
            GroupConfig(
                id="admin",
                name="Administration",
                description="System administration and settings",
                icon="cog",
                widgets=[
                    WidgetConfig(
                        id="settings",
                        name="Settings",
                        description="Dashboard configuration and preferences",
                        icon="sliders-h",
                        permissions=["admin.manage"],
                    )
                ],
            ),
        ],
        access_control=AccessControlConfig(
            default_permissions=[],
            roles={
                "admin": RoleConfig(
                    permissions=[
                        "analytics.view",
                        "analytics.performance",
                        "data_entry.edit",
                        "admin.manage",
                    ]
                ),
                "analyst": RoleConfig(
                    permissions=["analytics.view", "analytics.performance"]
                ),
                "data_entry": RoleConfig(permissions=["data_entry.edit"]),
                "viewer": RoleConfig(permissions=["analytics.view"]),
            },
            users={
                "alice": UserConfig(roles=["admin"]),
                "bob": UserConfig(roles=["analyst"]),
                "carol": UserConfig(roles=["data_entry"]),
                "dave": UserConfig(roles=["viewer"]),
            },
        ),
    )
