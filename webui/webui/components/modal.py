import reflex as rx
from webui.state import State


def modal() -> rx.Component:
    """A modal to create a new chat."""
    return rx.chakra.modal(
        rx.chakra.modal_overlay(
            rx.chakra.modal_content(
                rx.chakra.modal_header(
                    rx.chakra.hstack(
                        rx.chakra.text("Is your data hidden?"),
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
                        rx.box(
                            State.unprivate_text,
                            color="#fff",
                            max_width="100%",
                            background_color="#3b3b3b",
                            width="33vh",
                            height="50vh",
                            margin="10px",
                            padding="10px"
                        ),
                        rx.box(
                            State.private_dict_str,
                            color="#fff",
                            max_width="100%",
                            background_color="#3b3b3b",
                            width="33vh",
                            height="50vh",
                            margin="10px",
                            padding="10px"
                        ),
                        rx.box(
                            State.private_text,
                            color="#fff",
                            max_width="100%",
                            background_color="#3b3b3b",
                            width="33vh",
                            height="50vh",
                            margin="10px",
                            padding="10px"
                        )
                    )
                ),
                rx.chakra.modal_footer(
                    rx.chakra.button(
                        "Send",
                        bg="#5535d4",
                        box_shadow="md",
                        px="4",
                        py="2",
                        h="auto",
                        _hover={"bg": "#4c2db3"},
                        on_click=State.confirm_send_question,
                    ),
                ),
                bg="#222",
                color="#fff",
            ),
        ),
        is_open=State.modal_open,
    )
