# -*- coding: utf-8 -*-
"""Dashboard configuration."""
from models import (
    DashboardConfig,
    GroupConfig,
    WidgetConfig,
    AccessControlConfig,
    UserConfig,
    Role,
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
                groups=[
                    GroupConfig(
                        id="analytics.performance",
                        name="Performance",
                        description="System and application performance metrics",
                        widgets=[
                            WidgetConfig(
                                id="metrics",
                                name="System Metrics",
                                description="Real-time system health and performance metrics",
                                roles=[Role.ADMIN, Role.ANALYST],
                            )
                        ],
                    )
                ],
                widgets=[
                    WidgetConfig(
                        id="sales_dashboard",
                        name="Sales Dashboard",
                        description="Monthly and quarterly sales overview",
                        roles=[Role.ADMIN, Role.ANALYST, Role.VIEWER],
                    )
                ],
            ),
            GroupConfig(
                id="data_entry",
                name="Data Entry",
                description="Data input and management tools",
                widgets=[
                    WidgetConfig(
                        id="data_form",
                        name="Data Entry Form",
                        description="Standard data input forms",
                        roles=[Role.ADMIN, Role.DATA_ENTRY],
                    )
                ],
            ),
            GroupConfig(
                id="admin",
                name="Administration",
                description="System administration and settings",
                widgets=[
                    WidgetConfig(
                        id="settings",
                        name="Settings",
                        description="Dashboard configuration and preferences",
                        roles=[Role.ADMIN],
                    )
                ],
            ),
        ],
        access_control=AccessControlConfig(
            users={
                "alice": UserConfig(roles=[Role.ADMIN]),
                "bob": UserConfig(roles=[Role.ANALYST]),
                "carol": UserConfig(roles=[Role.DATA_ENTRY]),
                "dave": UserConfig(roles=[Role.VIEWER]),
            },
        ),
    )
