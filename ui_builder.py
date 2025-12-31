# -*- coding: utf-8 -*-
"""Dashboard UI builder with card-based navigation and lazy widget loading."""

# =============================================================================
# IMPORTS
# =============================================================================
import traceback
from typing import Callable, Dict, List
import ipywidgets as widgets
from ipyevents import Event
from IPython.display import display

from models import GroupConfig, WidgetConfig


# =============================================================================
# CONSTANTS & STYLES
# =============================================================================

# Card dimensions
CARD_WIDTH = "200px"
CARD_HEIGHT = "140px"
CARD_MARGIN = "10px"
CARD_BORDER_RADIUS = "20px"

# Colors for groups
GROUP_BG_COLOR = "#f0f4ff"
GROUP_BORDER_COLOR = "#667eea"

# Colors for widgets
WIDGET_BG_COLOR = "#e8f8f5"
WIDGET_BORDER_COLOR = "#17a2b8"

# Header styling
HEADER_BORDER_COLOR = "#667eea"


# =============================================================================
# CARD COMPONENTS
# =============================================================================

def create_card(
    title: str,
    description: str,
    icon: str,
    on_click: Callable,
    is_widget: bool = False
) -> widgets.Widget:
    """Create a clickable card using styled HTML with ipyevents.

    Args:
        title: Card title
        description: Card description (shown on hover)
        icon: Font Awesome icon name (without 'fa-' prefix)
        on_click: Callback function when card is clicked
        is_widget: True if this card represents a widget (vs a group)

    Returns:
        A clickable card widget
    """
    # Select colors based on type
    bg_color = WIDGET_BG_COLOR if is_widget else GROUP_BG_COLOR
    border_color = WIDGET_BORDER_COLOR if is_widget else GROUP_BORDER_COLOR

    # Create styled HTML card
    html_card = widgets.HTML(f'''
        <div style="
            width: {CARD_WIDTH};
            height: {CARD_HEIGHT};
            margin: {CARD_MARGIN};
            padding: 20px;
            background: {bg_color};
            border: 2px solid {border_color};
            border-radius: {CARD_BORDER_RADIUS};
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        "
        onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 20px rgba(0,0,0,0.15)';"
        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';"
        title="{description}">
            <i class="fa fa-{icon}" style="font-size: 2.5rem; color: {border_color}; margin-bottom: 10px;"></i>
            <span style="font-weight: bold; color: #333; text-align: center; font-size: 0.95rem;">{title}</span>
        </div>
    ''')

    # Attach click event using ipyevents
    event = Event(source=html_card, watched_events=['click'])
    event.on_dom_event(lambda e: on_click())

    # Wrap in container and keep event reference alive
    container = widgets.Box([html_card])
    container._event = event  # Prevent garbage collection

    return container


def create_card_grid(cards: List[widgets.Widget], columns: int = 3) -> widgets.Widget:
    """Create a responsive grid of cards.

    Args:
        cards: List of card widgets
        columns: Number of columns in grid (unused, using flex wrap)

    Returns:
        A widget containing the card grid
    """
    if not cards:
        return widgets.HTML(
            '<p style="color: #666; padding: 20px;">No items available.</p>'
        )

    return widgets.HBox(
        cards,
        layout=widgets.Layout(
            display="flex",
            flex_flow="row wrap",
            justify_content="flex-start",
            width="100%",
            padding="10px"
        )
    )


# =============================================================================
# HEADER & NAVIGATION COMPONENTS
# =============================================================================

def create_header(title: str, username: str) -> widgets.HTML:
    """Create the dashboard header with title and user info.

    Args:
        title: Dashboard title
        username: Current user's name

    Returns:
        Header HTML widget
    """
    return widgets.HTML(f'''
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            margin-bottom: 10px;
            border-bottom: 3px solid {HEADER_BORDER_COLOR};
        ">
            <h2 style="margin: 0; color: #333; font-size: 1.5rem;">
                {title}
            </h2>
            <span style="
                background: {HEADER_BORDER_COLOR};
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 0.9rem;
            ">
                User: {username}
            </span>
        </div>
    ''')


def create_breadcrumb(path: List[str]) -> widgets.HTML:
    """Create a breadcrumb navigation display.

    Args:
        path: List of navigation path items (e.g., ["Home", "Group1", "SubGroup"])

    Returns:
        Breadcrumb HTML widget
    """
    breadcrumb_html = " &gt; ".join(
        f'<span style="color: {HEADER_BORDER_COLOR};">{p}</span>' for p in path
    )

    return widgets.HTML(f'''
        <div style="
            padding: 10px 0;
            font-size: 0.95rem;
            color: #666;
        ">
            {breadcrumb_html}
        </div>
    ''')


def create_back_button(on_click: Callable) -> widgets.Widget:
    """Create a modern styled back navigation button.

    Args:
        on_click: Callback when button is clicked

    Returns:
        Back button widget (HTML with ipyevents)
    """
    html_btn = widgets.HTML('''
        <div style="
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 16px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.8rem;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
            transition: transform 0.2s, box-shadow 0.2s;
        "
        onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 12px rgba(102, 126, 234, 0.4)';"
        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(102, 126, 234, 0.3)';">
            <i class="fa fa-arrow-left"></i>
            <span>Back</span>
        </div>
    ''')

    event = Event(source=html_btn, watched_events=['click'])
    event.on_dom_event(lambda e: on_click())

    container = widgets.Box(
        [html_btn],
        layout=widgets.Layout(display='none', margin='0 10px 10px 0')
    )
    container._event = event  # Prevent garbage collection

    return container


def create_menu_button(on_click: Callable) -> widgets.Widget:
    """Create a modern styled menu button for returning from widget view.

    Args:
        on_click: Callback when button is clicked

    Returns:
        Menu button widget (HTML with ipyevents)
    """
    html_btn = widgets.HTML('''
        <div style="
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border-radius: 16px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.8rem;
            box-shadow: 0 2px 8px rgba(245, 87, 108, 0.3);
            transition: transform 0.2s, box-shadow 0.2s;
        "
        onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 12px rgba(245, 87, 108, 0.4)';"
        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(245, 87, 108, 0.3)';">
            <i class="fa fa-home"></i>
            <span>Menu</span>
        </div>
    ''')

    event = Event(source=html_btn, watched_events=['click'])
    event.on_dom_event(lambda e: on_click())

    container = widgets.Box(
        [html_btn],
        layout=widgets.Layout(display='none', margin='5px')
    )
    container._event = event  # Prevent garbage collection

    return container


# =============================================================================
# NAVIGATION CONTROLLER
# =============================================================================

class NavigationController:
    """Manages card navigation, breadcrumb, and lazy widget loading.

    This is the main orchestrator for the dashboard UI. It handles:
    - Navigation state (current location in group hierarchy)
    - Rendering cards for groups and widgets
    - Lazy loading widgets only when clicked
    - Full-screen widget view with menu button to return
    """

    def __init__(
        self,
        title: str,
        username: str,
        groups: List[GroupConfig],
        widget_registry: Dict[str, Callable]
    ):
        """Initialize the navigation controller.

        Args:
            title: Dashboard title
            username: Current user's name
            groups: List of root-level groups (already filtered by access)
            widget_registry: Dict mapping widget IDs to factory functions
        """
        self.title = title
        self.username = username
        self.root_groups = groups
        self.registry = widget_registry

        # Navigation state
        self.breadcrumb: List[GroupConfig] = []

        # UI components
        self._init_ui_components()

        # Initial render
        self._update_navigation()

    def _init_ui_components(self) -> None:
        """Initialize all UI component widgets."""
        self.header = create_header(self.title, self.username)
        self.breadcrumb_widget = widgets.HTML("")
        self.back_button = create_back_button(self.go_back)
        self.menu_button = create_menu_button(self.return_to_menu)
        self.cards_area = widgets.VBox([])
        self.content_area = widgets.VBox([])
        self.navigation_area = widgets.VBox([])

    # -------------------------------------------------------------------------
    # Navigation Methods
    # -------------------------------------------------------------------------

    def navigate_to_group(self, group: GroupConfig) -> None:
        """Navigate into a group.

        Args:
            group: The group to navigate into
        """
        self.breadcrumb.append(group)
        self._update_navigation()

    def go_back(self) -> None:
        """Navigate back to parent level."""
        if self.breadcrumb:
            self.breadcrumb.pop()
            self._update_navigation()

    def return_to_menu(self) -> None:
        """Return from widget view to card navigation."""
        self.navigation_area.layout.display = "block"
        self.menu_button.layout.display = "none"
        self.content_area.children = []

    # -------------------------------------------------------------------------
    # Widget Loading
    # -------------------------------------------------------------------------

    def load_widget(self, widget_config: WidgetConfig) -> None:
        """Lazy-load a widget into full-screen view.

        Args:
            widget_config: Configuration for the widget to load
        """
        # Hide navigation, show menu button
        self.navigation_area.layout.display = "none"
        self.menu_button.layout.display = "block"

        # Check if widget exists in registry
        if widget_config.id not in self.registry:
            self.content_area.children = [
                widgets.HTML(
                    f'<p style="color: red; padding: 20px;">'
                    f'Widget "{widget_config.id}" not found in registry.</p>'
                )
            ]
            return

        # Show loading indicator
        self.content_area.children = [
            widgets.HTML(
                '<div style="padding: 20px; text-align: center; color: #666;">'
                '<i class="fa fa-spinner fa-spin"></i> Loading widget...</div>'
            )
        ]

        # Create output widget to capture runtime errors from widget interactions
        output = widgets.Output()

        widget_factory = self.registry[widget_config.id]

        with output:
            try:
                widget_ui = widget_factory()
                display(widget_ui)
            except Exception:
                print(traceback.format_exc())

        self.content_area.children = [output]

    # -------------------------------------------------------------------------
    # Rendering Methods
    # -------------------------------------------------------------------------

    def _update_navigation(self) -> None:
        """Update breadcrumb and render cards for current level."""
        self._update_breadcrumb()
        self._render_cards()
        self.content_area.children = []

    def _update_breadcrumb(self) -> None:
        """Update the breadcrumb display."""
        path = ["Home"] + [g.name for g in self.breadcrumb]
        self.breadcrumb_widget.value = create_breadcrumb(path).value

        # Show/hide back button
        self.back_button.layout.display = "block" if self.breadcrumb else "none"

    def _render_cards(self) -> None:
        """Render cards for current navigation level."""
        cards = []

        if self.breadcrumb:
            # Inside a group - show its children
            current_group = self.breadcrumb[-1]
            cards.extend(self._create_group_cards(current_group.groups))
            cards.extend(self._create_widget_cards(current_group.widgets))
        else:
            # At root - show root groups
            cards.extend(self._create_group_cards(self.root_groups))

        self.cards_area.children = [create_card_grid(cards)]

    def _create_group_cards(self, groups: List[GroupConfig]) -> List[widgets.Widget]:
        """Create cards for a list of groups.

        Args:
            groups: List of group configurations

        Returns:
            List of card widgets
        """
        return [
            create_card(
                title=group.name,
                description=group.description,
                icon=group.icon,
                on_click=lambda g=group: self.navigate_to_group(g),
                is_widget=False
            )
            for group in groups
        ]

    def _create_widget_cards(self, widget_configs: List[WidgetConfig]) -> List[widgets.Widget]:
        """Create cards for a list of widgets.

        Args:
            widget_configs: List of widget configurations

        Returns:
            List of card widgets
        """
        return [
            create_card(
                title=wc.name,
                description=wc.description,
                icon=wc.icon,
                on_click=lambda w=wc: self.load_widget(w),
                is_widget=True
            )
            for wc in widget_configs
        ]

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def build_ui(self) -> widgets.Widget:
        """Build and return the complete dashboard UI.

        Returns:
            The root widget containing the entire dashboard
        """
        nav_bar = widgets.HBox([self.back_button, self.breadcrumb_widget])

        self.navigation_area.children = [
            self.header,
            nav_bar,
            self.cards_area
        ]

        return widgets.VBox([
            self.menu_button,      # Shown only when viewing widget
            self.navigation_area,  # Hidden when viewing widget
            self.content_area      # Widget renders here (full screen)
        ])
