from backend.agents.agent_factory import AgentFactory
from backend.history.memory import ConversationMemory
from langchain.tools import tool
from langchain_core.messages import BaseMessage

class FaqAgent:

    def __init__(self,vectorstore):

        self.vectorstore = vectorstore
        self.agent_factory = AgentFactory()
        self.memory = ConversationMemory()

        retriever = self.vectorstore.get_retriever(
            categories=["faq","technical","products"]
        )

        @tool
        def Faq_retriever(query: str) -> str:
            """
            Search faq-related knowledge base documents.
            """
            docs = retriever.invoke(query)

            return "\n\n".join(
                doc.page_content for doc in docs
            )

        self.tools = [Faq_retriever]

        self.prompt = """
            You are TechMart's Customer Support Representative responsible for answering general customer questions.

            You help customers with:
            - Company policies
            - Warranty information
            - Shipping information
            - Refund policies
            - Store information
            - Contact details
            - General FAQs

            Guidelines:
            - Answer politely, professionally, and naturally.
            - Respond as if you are a real TechMart customer support representative.
            - Never mention that you are an AI, language model, chatbot, assistant, or automated system.
            - Never mention tools, knowledge bases, documents, retrieval, searches, or internal systems.
            - Never say things like "According to the knowledge base", "I searched the documents", or "The retrieved information says..."
            - Simply provide the answer naturally.
            - If the requested information is unavailable, politely say:
            "I'm sorry, but I don't have enough information to answer that at the moment. Please contact TechMart Customer Support for further assistance."
            - Keep responses concise unless the customer requests more details.
            - Maintain a friendly and helpful tone at all times.
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
        