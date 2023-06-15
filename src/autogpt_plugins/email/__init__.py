"""This is the email plugin for Auto-GPT."""
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict
from auto_gpt_plugin_template import AutoGPTPluginTemplate
from colorama import Fore

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    role: str
    content: str


class AutoGPTEmailPlugin(AutoGPTPluginTemplate):
    """
    This is the Auto-GPT email plugin.
    """

    def __init__(self):
        super().__init__()
        self._name = "Auto-GPT-Email-Plugin"
        self._version = "0.1.3"
        self._description = "Auto-GPT Email Plugin: Supercharge email management."

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        from .email_plugin.email_plugin import (
            read_emails,
            draft_response,
            save_draft,
            bothEmailAndPwdSet,
        )

        if bothEmailAndPwdSet():
            prompt.add_command(
                "Read Emails",
                "read_emails",
                {
                    "imap_folder": "<imap_folder>",
                    "imap_search_command": "<imap_search_criteria_command>",
                },
                read_emails,
            )
            prompt.add_command(
                "Draft Response",
                "draft_response",
                {"email_content": "<email_content>"},
                draft_response,
            )
            prompt.add_command(
                "Save Draft",
                "save_draft",
                {"response_content": "<response_content>", "subject": "<subject>", "to": "<to>"},
                save_draft,
            )
        else:
            print(
                Fore.RED
                + f"{self._name} - {self._version} - Email plugin not loaded, because EMAIL_PASSWORD or EMAIL_ADDRESS were not set in env."
            )

        return prompt

    def can_handle_post_prompt(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_prompt method.

        Returns:
            bool: True if the plugin can handle the post_prompt method."""
        return True

    # For remaining methods that are not necessary for your use-case, we return False or None as appropriate.

    def can_handle_on_response(self) -> bool:
        return False

    def on_response(self, response: str, *args, **kwargs) -> str:
        pass

    def can_handle_on_planning(self) -> bool:
        return False

    def on_planning(
        self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        pass

    def can_handle_post_planning(self) -> bool:
        return False

    def post_planning(self, response: str) -> str:
        pass

    def can_handle_pre_instruction(self) -> bool:
        return False

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        pass

    def can_handle_on_instruction(self) -> bool:
        return False

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        pass

    def can_handle_post_instruction(self) -> bool:
        return False

    def post_instruction(self, response: str) -> str:
        pass

    def can_handle_pre_command(self) -> bool:
        return False

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        pass

    def can_handle_post_command(self) -> bool:
        return False

    def post_command(self, command_name: str, response: str) -> str:
        pass

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        return False

    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        pass
