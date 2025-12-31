# -*- coding: utf-8 -*-
"""Card-based UI builder with lazy loading and drill-down navigation."""
from typing import Callable, Dict, List, Optional
import ipywidgets as widgets

from models import GroupConfig, WidgetConfig


def create_card(
    title: str,
    description: str,
    icon: str,
    on_click: Callable,
    is_widget: bool = False
) -> widgets.Widget:
    """Create a clickable card using a styled Button widget.

    Args:
        title: Card title
        description: Card description
        icon: Font Awesome icon name (without 'fa-' prefix)
        on_click: Callback function when card is clicked
        is_widget: True if this card represents a widget (vs a group)

    Returns:
        A clickable card widget
    """
    # Colors for groups vs widgets
    bg_color = "#f8f9fa" if not is_widget else "#e8f4f8"
    border_color = "#667eea" if not is_widget else "#17a2b8"
    icon_color = "#667eea" if not is_widget else "#17a2b8"

    # Truncate description
    short_desc = description[:50] + '...' if len(description) > 50 else description

    # Generate unique ID for this card's styles
    import random
    card_id = f"card_{random.randint(10000, 99999)}"

    # Create Output widget - this lets us render custom HTML that's also clickable
    output = widgets.Output(
        layout=widgets.Layout(
            width="220px",
            height="160px",
            margin="10px",
        )
    )

    with output:
        from IPython.display import display, HTML
        display(HTML(f'''
            <style>
                #{card_id} {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    width: 200px;
                    height: 150px;
                    padding: 15px;
                    text-align: center;
                    cursor: pointer;
                    background: {bg_color};
                    border: 2px solid {border_color};
                    border-radius: 12px;
                    box-sizing: border-box;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    user-select: none;
                }}
                #{card_id}:hover {{
                    transform: translateY(-4px);
                    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                }}
                #{card_id}:active {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                }}
            </style>
            <div id="{card_id}">
                <div style="font-size: 2.5rem; color: {icon_color}; margin-bottom: 10px;">
                    <i class="fa fa-{icon}"></i>
                </div>
                <div style="font-weight: 600; font-size: 1.1rem; color: #333; margin-bottom: 6px;">
                    {title}
                </div>
                <div style="font-size: 0.8rem; color: #666; line-height: 1.4;">
                    {short_desc}
                </div>
            </div>
        '''))

    # Invisible button on top for click handling
    button = widgets.Button(
        description="",
        tooltip=f"{title}: {description}",
        layout=widgets.Layout(
            width="220px",
            height="160px",
            margin="-160px 0 0 0",  # Pull up to overlap
            opacity="0",
        )
    )
    button.on_click(lambda b: on_click())

    return widgets.VBox(
        [output, button],
        layout=widgets.Layout(
            width="220px",
            height="160px",
            margin="10px",
        )
    )


def create_card_grid(cards: List[widgets.Widget], columns: int = 3) -> widgets.Widget:
    """Create a responsive grid of cards.

    Args:
        cards: List of card widgets
        columns: Number of columns in grid

    Returns:
        A widget containing the card grid
    """
    if not cards:
        return widgets.HTML(
            '<p style="color: #666; padding: 20px;">No items available.</p>'
        )

    # Create rows
    rows = []
    for i in range(0, len(cards), columns):
        row_cards = cards[i:i + columns]
        row = widgets.HBox(
            row_cards,
            layout=widgets.Layout(
                display="flex",
                flex_flow="row wrap",
                justify_content="flex-start",
            )
        )
        rows.append(row)

    return widgets.VBox(
        rows,
        layout=widgets.Layout(width="100%", padding="10px")
    )


class NavigationController:
    """Manages card navigation, breadcrumb, and lazy widget loading."""

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
        self.current_items: List[GroupConfig] = groups

        # UI components
        self.header = self._create_header()
        self.breadcrumb_widget = widgets.HTML("")
        self.back_button = self._create_back_button()
        self.home_button = self._create_home_button()  # Small button for widget view
        self.cards_area = widgets.VBox([])
        self.content_area = widgets.VBox([])
        self.navigation_area = widgets.VBox([])  # Holds header, nav, cards

        # Track if we're viewing a widget
        self.viewing_widget = False

        # Initial render
        self._update_breadcrumb()
        self._render_cards()

    def _create_header(self) -> widgets.HTML:
        """Create the dashboard header."""
        return widgets.HTML(f'''
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 0;
                margin-bottom: 10px;
                border-bottom: 3px solid #667eea;
            ">
                <h2 style="margin: 0; color: #333; font-size: 1.5rem;">
                    {self.title}
                </h2>
                <span style="
                    background: #667eea;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 0.9rem;
                ">
                    User: {self.username}
                </span>
            </div>
        ''')

    def _create_back_button(self) -> widgets.Button:
        """Create the back navigation button."""
        btn = widgets.Button(
            description="Back",
            icon="arrow-left",
            button_style="info",
            layout=widgets.Layout(width="100px", margin="0 10px 10px 0")
        )
        btn.on_click(lambda b: self.go_back())
        return btn

    def _create_home_button(self) -> widgets.Button:
        """Create a small home button for returning from widget view."""
        btn = widgets.Button(
            description="Menu",
            icon="home",
            button_style="warning",
            layout=widgets.Layout(width="80px", margin="5px", display="none")
        )
        btn.on_click(lambda b: self.return_to_menu())
        return btn

    def _update_breadcrumb(self) -> None:
        """Update the breadcrumb display."""
        parts = ["Home"]
        for group in self.breadcrumb:
            parts.append(group.name)

        breadcrumb_html = " &gt; ".join(
            f'<span style="color: #667eea;">{p}</span>' for p in parts
        )

        self.breadcrumb_widget.value = f'''
            <div style="
                padding: 10px 0;
                font-size: 0.95rem;
                color: #666;
            ">
                {breadcrumb_html}
            </div>
        '''

        # Show/hide back button based on navigation depth
        self.back_button.layout.display = "block" if self.breadcrumb else "none"

    def _render_cards(self) -> None:
        """Render cards for current navigation level."""
        cards = []

        # Get current group (if navigated into one)
        if self.breadcrumb:
            current_group = self.breadcrumb[-1]
            # Show sub-groups
            for group in current_group.groups:
                card = self._create_group_card(group)
                cards.append(card)
            # Show widgets
            for widget_config in current_group.widgets:
                card = self._create_widget_card(widget_config)
                cards.append(card)
        else:
            # Show root groups
            for group in self.root_groups:
                card = self._create_group_card(group)
                cards.append(card)

        grid = create_card_grid(cards, columns=3)
        self.cards_area.children = [grid]

        # Clear content area when navigating
        self.content_area.children = []

    def _create_group_card(self, group: GroupConfig) -> widgets.Widget:
        """Create a card for a group."""
        return create_card(
            title=group.name,
            description=group.description,
            icon=group.icon,
            on_click=lambda g=group: self.navigate_to_group(g),
            is_widget=False
        )

    def _create_widget_card(self, widget_config: WidgetConfig) -> widgets.Widget:
        """Create a card for a widget."""
        return create_card(
            title=widget_config.name,
            description=widget_config.description,
            icon=widget_config.icon,
            on_click=lambda w=widget_config: self.load_widget(w),
            is_widget=True
        )

    def navigate_to_group(self, group: GroupConfig) -> None:
        """Navigate into a group."""
        self.breadcrumb.append(group)
        self._update_breadcrumb()
        self._render_cards()

    def go_back(self) -> None:
        """Navigate back to parent level."""
        if self.breadcrumb:
            self.breadcrumb.pop()
            self._update_breadcrumb()
            self._render_cards()

    def return_to_menu(self) -> None:
        """Return from widget view to card navigation."""
        self.viewing_widget = False
        # Show navigation, hide home button
        self.navigation_area.layout.display = "block"
        self.home_button.layout.display = "none"
        # Clear widget content
        self.content_area.children = []

    def load_widget(self, widget_config: WidgetConfig) -> None:
        """Lazy-load a widget into the content area (full screen mode)."""
        self.viewing_widget = True

        # Hide navigation, show home button
        self.navigation_area.layout.display = "none"
        self.home_button.layout.display = "block"

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

        # Create the widget
        try:
            widget_factory = self.registry[widget_config.id]
            widget_ui = widget_factory()

            # Full screen - just the widget, no header
            self.content_area.children = [widget_ui]

        except Exception as e:
            self.content_area.children = [
                widgets.HTML(
                    f'<p style="color: red; padding: 20px;">'
                    f'Error loading widget: {str(e)}</p>'
                )
            ]

    def build_ui(self) -> widgets.Widget:
        """Build and return the complete dashboard UI."""
        nav_bar = widgets.HBox([
            self.back_button,
            self.breadcrumb_widget
        ])

        # Group navigation elements together so they can be hidden/shown as one
        self.navigation_area.children = [
            self.header,
            nav_bar,
            self.cards_area
        ]

        return widgets.VBox([
            self.home_button,      # Shown only when viewing widget
            self.navigation_area,  # Hidden when viewing widget
            self.content_area      # Widget renders here (full screen)
        ])
