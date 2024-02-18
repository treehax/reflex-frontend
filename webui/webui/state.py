import os
import requests
import json
import openai
import reflex as rx

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")


if not openai.api_key and not BAIDU_API_KEY:
    raise Exception("Please set OPENAI_API_KEY or BAIDU_API_KEY")


def get_access_token():
    """
    :return: access_token
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_API_KEY,
        "client_secret": BAIDU_SECRET_KEY,
    }
    return str(requests.post(url, params=params).json().get("access_token"))


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Chat": [],
}

from typing import List, Dict


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: Dict[str, List[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Chat"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    # Whether the drawer is open.
    drawer_open: bool = False

    # Whether the modal is open.
    modal_open: bool = False

    unprivate_text: str = ""

    private_text: str = ""

    private_dict_str: str = ""

    private_dict: dict = {}

    api_type: str = "baidu" if BAIDU_API_KEY else "openai"

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

        # Toggle the modal.
        self.modal_open = False

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()

    @rx.var
    def chat_titles(self) -> List[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def confirm_send_question(self):
        question = self.private_text
        self.modal_open = False
        self.processing = True

        # Add the question to the list of questions.
        qa = QA(question=self.unprivate_text, answer="")
        self.chats[self.current_chat].append(qa)

        # Start a new session to answer the question.
        response = requests.post(
            "https://151e-68-65-175-22.ngrok-free.app/ai/",
            json={"bare_prompt": question},
            headers={"Content-Type": "application/json", "accept": "application/json"},
        )

        data = response.json()

        # api request - censored_prompt, censoring_dict
        response = requests.post(
            "https://151e-68-65-175-22.ngrok-free.app/ai/uncensor",
            json={
                "censored_prompt": data["message"]["content"],
                "censoring_dict": dict(self.private_dict),
            },
            headers={"Content-Type": "application/json", "accept": "application/json"},
        )

        data = response.json()

        self.chats[self.current_chat][-1].answer = data
        self.chats = self.chats

        # Toggle the processing flag.
        self.processing = False

    async def process_question(self, form_data: Dict[str, str]):
        # Get the question from the form
        question = form_data["question"]
        if question == None:
            return

        self.modal_open = True
        self.private_dict_str = "Loading..."
        self.private_text = "Loading..."

        # Check if the question is empty
        if question == "":
            return

        if self.api_type == "openai":
            model = self.openai_process_question
        else:
            model = self.baidu_process_question

        async for value in model(question):
            yield value

    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """

        self.unprivate_text = question

        # Clear the input and start the processing.
        self.processing = True
        yield

        response = requests.post(
            "https://151e-68-65-175-22.ngrok-free.app/ai/replacement",
            json={"insecure_prompt": question},
            headers={"Content-Type": "application/json", "accept": "application/json"},
        )

        data = response.json()
        self.private_dict = data
        self.private_dict_str = ""
        for key, val in data.items():
            self.private_dict_str += key + " → " + val + "\n"

        if self.private_dict_str == "":
            self.private_dict_str = "No replacements!"

        self.private_text = self.unprivate_text
        for key in data.keys():
            self.private_text = self.private_text.replace(key, data[key])

        # Toggle the processing flag.
        self.processing = False

    async def baidu_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = []
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = json.dumps({"messages": messages[:-1]})
        # Start a new session to answer the question.
        session = requests.request(
            "POST",
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token="
            + get_access_token(),
            headers={"Content-Type": "application/json"},
            data=messages,
        )

        json_data = json.loads(session.text)
        if "result" in json_data.keys():
            answer_text = json_data["result"]
            self.chats[self.current_chat][-1].answer += answer_text
            self.chats = self.chats
            yield
        # Toggle the processing flag.
        self.processing = False


def fetch_history():
    """return {
        "history": [
            {
                "sanitized_prompt": "Write an email telling Rob he has HPV",
                "proofs": [123, 456, 789],
                "proven": True,
            },
            {
                "sanitized_prompt": "Write python "
                "code that connects to the OpenAI API with my API key sk_123abc123",
                "proofs": [123, 456, 789],
                "proven": True,
            },
            {
                "sanitized_prompt": "My patient name=John Doe is 5'11 and has a BMI of 28, with a diagnosis of hypertension. Write a formal note for the insurance company",
                "proofs": [123, 456, 789],
                "proven": False,
            },
        ],
    }
    """
    history_request = requests.get(
        "https://151e-68-65-175-22.ngrok-free.app/ai/history"
    )
    history = history_request.json()
    # Turn this into just a list of lists that contain the values
    clean_history = []
    for item in history["history"]:
        clean_history.append(
            [
                item["sanitized_prompt"],
                item["proofs"],
                str(item["proven"]),
            ]
        )
    return clean_history


class AdminState(rx.State):
    history: List[str]
    columns: List[str] = ["Prompt", "Proofs", "Proven"]

    def get_data(self):
        self.history = fetch_history()
        print(self.history)
