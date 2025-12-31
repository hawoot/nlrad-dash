# -*- coding: utf-8 -*-
"""Data models for dashboard configuration."""
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class WidgetConfig:
    """Configuration for a single widget."""
    id: str
    name: str
    description: str = ""
    icon: str = "cube"
    roles: List[str] = field(default_factory=list)  # roles that can access this widget


@dataclass
class GroupConfig:
    """Configuration for a widget group (supports nesting)."""
    id: str
    name: str
    description: str = ""
    icon: str = "folder"
    groups: List['GroupConfig'] = field(default_factory=list)
    widgets: List[WidgetConfig] = field(default_factory=list)


@dataclass
class UserConfig:
    """User-specific access configuration."""
    roles: List[str] = field(default_factory=list)


@dataclass
class AccessControlConfig:
    """Access control configuration."""
    users: Dict[str, UserConfig] = field(default_factory=dict)


@dataclass
class DashboardConfig:
    """Root configuration object."""
    version: str
    title: str
    groups: List[GroupConfig]
    access_control: AccessControlConfig
    description: str = ""
