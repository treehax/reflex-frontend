import reflex as rx

from webui import styles
from webui.components import loading_icon
from webui.state import QA, State


def message(qa: QA) -> rx.Component:
    """A single question/answer message.

    Args:
        qa: The question/answer pair.

    Returns:
        A component displaying the question/answer pair.
    """
    return rx.chakra.box(
        rx.chakra.box(
            rx.chakra.text(
                qa.question,
                bg=styles.border_color,
                shadow=styles.shadow_light,
                **styles.message_style,
            ),
            text_align="right",
            margin_top="1em",
        ),
        rx.chakra.box(
            rx.chakra.text(
                qa.answer,
                bg=styles.accent_color,
                shadow=styles.shadow_light,
                **styles.message_style,
            ),
            text_align="left",
            padding_top="1em",
        ),
        width="100%",
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.chakra.vstack(
        rx.chakra.box(rx.foreach(State.chats[State.current_chat], message), on_mouse_enter=State.change_chat_mouse_enter, on_mouse_leave=State.change_chat_mouse_leave),
        py="8",
        flex="1",
        width="100%",
        max_w="3xl",
        padding_x="4",
        align_self="center",
        overflow="hidden",
        padding_bottom="5em",
    )


def action_bar() -> rx.Component:
    """The action bar to send a new message."""
    return rx.chakra.box(
        rx.chakra.vstack(
            rx.chakra.form(
                rx.chakra.form_control(
                    rx.chakra.hstack(
                        rx.chakra.input(
                            placeholder="Type something...",
                            id="question",
                            _placeholder={"color": "#fffa"},
                            _hover={"border_color": styles.accent_color},
                            style=styles.input_style,
                        ),
                        rx.chakra.button(
                            rx.cond(
                                State.processing,
                                loading_icon(height="1em"),
                                rx.chakra.text("Send"),
                            ),
                            type_="submit",
                            _hover={"bg": styles.accent_color},
                            style=styles.input_style,
                        ),
                    ),
                    is_disabled=State.processing,
                ),
                on_submit=State.process_question,
                reset_on_submit=True,
                width="100%",
            ),
            rx.chakra.text(
                "CloakAI",
                font_size="xs",
                color="#fff6",
                text_align="center",
            ),
            width="100%",
            max_w="3xl",
            mx="auto",
        ),
        position="sticky",
        bottom="0",
        left="0",
        py="4",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid {styles.border_color}",
        align_items="stretch",
        width="100%",
    )
