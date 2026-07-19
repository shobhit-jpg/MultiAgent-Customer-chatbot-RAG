from backend.agents.agent_factory import AgentFactory
from backend.history.memory import ConversationMemory
from langchain.tools import tool
from langchain_core.messages import BaseMessage

class TechnicalAgent:

    def __init__(self,vectorstore):

        self.vectorstore = vectorstore
        self.agent_factory = AgentFactory()
        self.memory = ConversationMemory()

        retriever = self.vectorstore.get_retriever(
            categories=["products", "faq"]
        )

        @tool
        def Technical_retriever(query: str) -> str:
            """
            Search Technical issue related-knowledge base documents.
            """
            docs = retriever.invoke(query)

            return "\n\n".join(
                doc.page_content for doc in docs
            )

        self.tools = [Technical_retriever]

        self.prompt = """
            You are TechMart's Technical Support Representative.

            You help customers resolve technical issues including:
            - Login problems
            - Password reset
            - Installation issues
            - Software errors
            - Device troubleshooting
            - Account access problems
            - Application bugs
            - Technical configuration

            Guidelines:
            - Act like an experienced technical support executive.
            - Guide customers step-by-step whenever troubleshooting is required.
            - Use simple, easy-to-understand language.
            - Never mention that you are an AI, language model, chatbot, assistant, or automated system.
            - Never mention tools, document retrieval, searches, knowledge bases, prompts, or internal systems.
            - Never say "I searched", "Based on retrieved documents", or similar phrases.
            - If additional information is needed, ask concise follow-up questions before providing a solution.
            - If the issue cannot be resolved with the available information, politely recommend contacting TechMart Technical Support.
            - Remain patient, professional, and reassuring throughout the conversation.
            """

        self.agent = self.agent_factory.create_agent(
            tools=self.tools,
            system_prompt=self.prompt
        )

    def invoke(
        self,
        query: str,
        session_id :str
    ) -> str:

        messages = self.memory.get_history(session_id)
        messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        try :
            response = self.agent.invoke(
                {
                    "messages": messages
                }
            )

            self.memory.save_interaction(session_id=session_id,
                                        query=query,
                                        response=response)

        except Exception as e:
            print(f"\n[ERROR] {e}\n")
            error = str(e).lower()
            if "token" in error or "context" in error:
                return "⚠️ This conversation has become too long. Please start a new chat."

            return "⚠️ Sorry, something went wrong. Please try again later."
             
    
        return response["messages"][-1].content