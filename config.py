# -*- coding: utf-8 -*-
"""Dashboard configuration."""
from models import (
    DashboardConfig,
    GroupConfig,
    WidgetConfig,
    AccessControlConfig,
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
                                roles=["admin", "analyst"],
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
                        roles=["admin", "analyst", "viewer"],
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
                        roles=["admin", "data_entry"],
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
                        roles=["admin"],
                    )
                ],
            ),
        ],
        access_control=AccessControlConfig(
            users={
                "alice": UserConfig(roles=["admin"]),
                "bob": UserConfig(roles=["analyst"]),
                "carol": UserConfig(roles=["data_entry"]),
                "dave": UserConfig(roles=["viewer"]),
            },
        ),
    )
