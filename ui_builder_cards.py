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
) -> widgets.Button:
    """Create a clickable card styled as a button.

    Args:
        title: Card title
        description: Card description
        icon: Font Awesome icon name (without 'fa-' prefix)
        on_click: Callback function when card is clicked
        is_widget: True if this card represents a widget (vs a group)

    Returns:
        A styled Button widget
    """
    # Use different colors for groups vs widgets
    bg_color = "#f8f9fa" if not is_widget else "#e8f4f8"
    border_color = "#667eea" if not is_widget else "#17a2b8"
    icon_color = "#667eea" if not is_widget else "#17a2b8"

    card = widgets.Button(
        description="",
        tooltip=f"{title}: {description}",
        layout=widgets.Layout(
            width="200px",
            height="150px",
            margin="8px",
            border=f"2px solid {border_color}",
            border_radius="12px",
        )
    )

    # We'll use HTML overlay for the card content
    card_content = widgets.HTML(f'''
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            background: {bg_color};
            border-radius: 10px;
        ">
            <div style="font-size: 2rem; color: {icon_color}; margin-bottom: 10px;">
                <i class="fa fa-{icon}"></i>
            </div>
            <div style="font-weight: 600; font-size: 1rem; margin-bottom: 5px; color: #333;">
                {title}
            </div>
            <div style="font-size: 0.8rem; color: #666; line-height: 1.3;">
                {description[:50] + '...' if len(description) > 50 else description}
            </div>
        </div>
    ''')

    card.on_click(lambda b: on_click())

    # Stack button and HTML content
    return widgets.VBox(
        [card_content, card],
        layout=widgets.Layout(
            width="200px",
            height="150px",
            margin="8px",
            position="relative",
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
        self.cards_area = widgets.VBox([])
        self.content_area = widgets.VBox([])

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

    def load_widget(self, widget_config: WidgetConfig) -> None:
        """Lazy-load a widget into the content area."""
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

            # Wrap with header
            widget_header = widgets.HTML(f'''
                <div style="
                    padding: 15px;
                    background: #f8f9fa;
                    border-left: 4px solid #17a2b8;
                    margin: 20px 0 10px 0;
                ">
                    <h3 style="margin: 0 0 5px 0; color: #333;">
                        <i class="fa fa-{widget_config.icon}" style="color: #17a2b8;"></i>
                        {widget_config.name}
                    </h3>
                    <p style="margin: 0; color: #666; font-size: 0.9rem;">
                        {widget_config.description}
                    </p>
                </div>
            ''')

            self.content_area.children = [widget_header, widget_ui]

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

        return widgets.VBox([
            self.header,
            nav_bar,
            self.cards_area,
            self.content_area
        ])
