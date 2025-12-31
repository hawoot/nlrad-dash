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
    permissions: List[str] = field(default_factory=list)


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
class RoleConfig:
    """Configuration for a user role."""
    permissions: List[str] = field(default_factory=list)


@dataclass
class UserConfig:
    """User-specific access configuration."""
    roles: List[str] = field(default_factory=list)
    additional_permissions: List[str] = field(default_factory=list)


@dataclass
class AccessControlConfig:
    """Full access control configuration."""
    default_permissions: List[str] = field(default_factory=list)
    roles: Dict[str, RoleConfig] = field(default_factory=dict)
    users: Dict[str, UserConfig] = field(default_factory=dict)


@dataclass
class DashboardConfig:
    """Root configuration object."""
    version: str
    title: str
    groups: List[GroupConfig]
    access_control: AccessControlConfig
    description: str = ""
