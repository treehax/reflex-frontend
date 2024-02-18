"""The main Chat app."""

import reflex as rx

from webui import styles
from webui.components import chat, modal, navbar, sidebar
from webui.state import AdminState, State


def index() -> rx.Component:
    """The main app."""
    return rx.chakra.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        sidebar(),
        modal(),
        bg=styles.bg_dark_color,
        color=styles.text_light_color,
        min_h="100vh",
        align_items="stretch",
        spacing="0",
    )


def admin() -> rx.Component:
    """The admin panel."""
    return rx.vstack(
        rx.data_table(
            data=AdminState.history,
            columns=AdminState.columns,
        ),
        rx.button(
            "Verify",
            padding="10px",
            margin="10px",
            background_color="#d43552",
            size="3",
            align="center",
            width="100px",
            height="40px",
            on_click=AdminState.verify
        ),
        align="center",
    )


# Add state and page to the app.
app = rx.App(style=styles.base_style)
app.add_page(index)
app.add_page(admin, on_load=AdminState.get_data)
