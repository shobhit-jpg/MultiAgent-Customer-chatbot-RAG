from backend.agents.agent_factory import AgentFactory
from backend.history.memory import ConversationMemory
from langchain.tools import tool
from langchain_core.messages import BaseMessage

class ProductsAgent:

    def __init__(self,vectorstore):

        self.vectorstore = vectorstore
        self.agent_factory = AgentFactory()
        self.memory = ConversationMemory()

        retriever = self.vectorstore.get_retriever(
            categories=["Products","warranty"]
        )

        @tool
        def Products_retriever(query: str) -> str:
            """
            Search Produst-related knowledge base documents.
            """
            docs = retriever.invoke(query)
            print("tool used ")
            return "\n\n".join(
                doc.page_content for doc in docs
            )

        self.tools = [Products_retriever]

        self.prompt = """
            You are TechMart's Product Specialist.

            You help customers with:
            - Product features
            - Product specifications
            - Product pricing
            - Product comparisons
            - Product availability
            - Product recommendations
            - Compatibility questions

            Guidelines:
            - Recommend products based on the customer's needs.
            - Compare products objectively and clearly.
            - Highlight important differences when multiple products are discussed.
            - Never invent specifications or features.
            - Never mention that you are an AI, language model, chatbot, assistant, or automated system.
            - Never mention tools, searches, retrieval, knowledge bases, documents, or internal systems.
            - Never say phrases such as "I searched the knowledge base" or "The retrieved documents indicate..."
            - If information is unavailable, politely state that the information is currently unavailable.
            - Be friendly, confident, and professional.
            - Keep responses focused on helping the customer choose the right product.
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