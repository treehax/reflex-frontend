import reflex as rx
from webui.state import State
from webui import styles


def modal() -> rx.Component:
    """A modal to create a new chat."""
    return rx.chakra.modal(
        rx.chakra.modal_overlay(
            # rx.chakra.modal_content(
                rx.chakra.modal_header(
                    rx.chakra.hstack(
                        rx.chakra.text(
                            "Is your data hidden?",
                            font_size="4xl"
                        ),
                        rx.chakra.icon(
                            tag="close",
                            font_size="sm",
                            on_click=State.toggle_modal,
                            color="#fff8",
                            _hover={"color": "#fff"},
                            cursor="pointer",
                        ),
                        align_items="center",
                        justify_content="space-between",
                    )
                ),
                rx.chakra.modal_body(
                    rx.hstack(
                        rx.vstack(
                            rx.heading(
                                "Original text",
                                font_size="4xl"
                            ),
                            rx.box(
                                State.unprivate_text,
                                color="#fff",
                                background_color="#363636",
                                height="50vh",
                                margin="10px",
                                padding="20px",
                                width="100%",
                                # width="33%",
                                border_radius="15px",
                            ),
                            margin="10px",
                            width="33%",
                        ),
                        rx.vstack(
                            rx.heading(
                                "Privacy Changes",
                                font_size="4xl"
                            ),
                            rx.box(
                                State.private_dict_str,
                                color="#fff",
                                background_color="#363636",
                                height="50vh",
                                width="100%",
                                margin="10px",
                                padding="20px",
                                border_radius="15px"
                            ),
                            width="33%",
                            margin="10px",
                        ),
                        rx.vstack(
                            rx.heading(
                                "Text sent to LLM",
                                font_size="4xl"
                            ),
                            rx.box(
                                State.private_text,
                                color="#fff",
                                background_color="#363636",
                                height="50vh",
                                margin="10px",
                                width="100%",
                                padding="20px",
                                border_radius="15px"
                            ),
                            width="33%",
                            margin="10px",
                        )
                    )
                ),
                rx.chakra.modal_footer(
                    rx.chakra.button(
                        "Send",
                        bg="#d43552",
                        box_shadow="md",
                        px="4",
                        py="2",
                        h="auto",
                        font_size="xl",
                        _hover={"bg": "#b32d41"},
                        on_click=State.confirm_send_question,
                    ),
                ),
                bg="#222",
                color="#fff",
                width="100vw",
                height="100vh",
            # ),
        ),
        is_open=State.modal_open,
    )
