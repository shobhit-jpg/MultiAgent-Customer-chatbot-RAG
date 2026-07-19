from typing import Literal
from pydantic import BaseModel
from backend.agents.agent_factory import AgentFactory
from backend.history.memory import ConversationMemory
from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)


class IntentLabel(BaseModel):
    """
    Structured output for intent classification.
    """

    intent: Literal[
        "escalate"
        "billing",
        "technical",
        "product",
        "complaint",
        "faq"
    ]


class IntentAgent:

    def __init__(self):

        self.agent_factory = AgentFactory()
        self.memory = ConversationMemory()
        self.llm = self.agent_factory.llm.with_structured_output(
            IntentLabel
        )

        self.system_prompt = """
                You are an Intent Classification Agent.

                Your job is to classify the user's query into EXACTLY ONE of the following intents:

                - billing
                - technical
                - product
                - complaint
                - faq
                - escalate

                Classification Rules:

                • billing
                - Refunds
                - Payments
                - Billing issues
                - Invoices
                - Subscription

                • technical
                - Installation
                - Login issues
                - Errors
                - Troubleshooting
                - Software problems

                • product
                - Product information
                - Features
                - Specifications
                - Comparisons

                • complaint
                - Negative feedback
                - Poor service
                - Damaged product
                - Bad experience

                • faq
                - General questions
                - Company information
                - Policies
                - Anything not covered above

                • escalate
                - The user explicitly requests a human agent, representative, or manager.
                - The issue requires manual verification or human intervention.
                - The customer repeatedly states that the issue is unresolved.
                - The customer is extremely frustrated or dissatisfied.
                - The query cannot be confidently classified into any other intent.

                Return ONLY one of the following words:

                billing
                technical
                product
                complaint
                faq
                escalate

        """

    def detect_intent(self, query: str, session_id: str) -> str:

        history = self.memory.get_history(session_id, count=3)

        messages = [
            SystemMessage(content=self.system_prompt),
            *history,
            HumanMessage(content=query)
        ]
        try :
            response = self.llm.invoke(messages)
        except Exception as e :
            print(f"\n[ERROR] {e}\n")
            error = str(e).lower()
            if "token" in error or "context" in error:
                return "⚠️ This conversation has become too long. Please start a new chat."

            return "⚠️ Sorry, something went wrong. Please try again later."
        
        return response.intent