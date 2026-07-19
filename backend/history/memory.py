from uuid import uuid4
from datetime import datetime, timezone
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    BaseMessage,
)
from backend.history.mongodb import mongodb
class ConversationMemory:

    def __init__(self, max_history: int = 10):
        self.collection = mongodb.conversations
        self.max_history = max_history

    def new_chat(self) -> str:
        """
        Creates a new conversation and returns its session ID.
        """
        session_id = str(uuid4())

        conversation = {
            "session_id": session_id,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "messages": []
        }

        self.collection.insert_one(conversation)

        return session_id
    
    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
        ) -> bool:
        """
        Add a message to an existing conversation.
        """

        if role not in ["user", "assistant"]:
            raise ValueError("Role must be 'user' or 'assistant'")

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc)
        }

        result = self.collection.update_one(
            {"session_id": session_id},
            {
                "$push": {
                    "messages": message
                },
                "$set": {
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )

        return result.modified_count > 0

    def save_interaction(
        self,
        session_id: str,
        query: str,
        response: dict
    ) -> bool:
        """
        Save both the user query and the assistant response
        from an agent invocation.
        """

        messages = [
            {
                "role": "user",
                "content": query,
                "timestamp": datetime.now(timezone.utc)
            },
            {
                "role": "assistant",
                "content": response["messages"][-1].content,
                "timestamp": datetime.now(timezone.utc)
            }
        ]

        result = self.collection.update_one(
            {"session_id": session_id},
            {
                "$push": {
                    "messages": {
                        "$each": messages
                    }
                },
                "$set": {
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )

        return result.modified_count > 0

    def get_history(
        self,
        session_id: str,
        count = 10
    ) -> list[BaseMessage]:
        """
        Returns the last N messages as LangChain messages.
        """

        conversation = self.collection.find_one(
            {"session_id": session_id}
        )

        if conversation is None:
            return []

        history = []
        messages = conversation["messages"][-count:]

        for message in messages:

            if message["role"] == "user":
                history.append(
                    HumanMessage(
                        content=message["content"]
                    )
                )

            elif message["role"] == "assistant":
                history.append(
                    AIMessage(
                        content=message["content"]
                    )
                )

        return history

    def get_chat(self, session_id: str):
        """
        Returns the complete MongoDB conversation document.
        """

        return self.collection.find_one(
            {"session_id": session_id},
            {"_id": 0}
        )

    def list_chats(self):
        """
        Returns all conversations.
        """

        chats = self.collection.find(
            {},
            {
                "_id": 0,
                "session_id": 1,
                "created_at": 1,
                "updated_at": 1
            }
        )

        return list(chats)

    def delete_chat(self, session_id: str) -> bool:
        """
        Deletes a conversation.
        """

        result = self.collection.delete_one(
            {"session_id": session_id}
        )

        return result.deleted_count > 0