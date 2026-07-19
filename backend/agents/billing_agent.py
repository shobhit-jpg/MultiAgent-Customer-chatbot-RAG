from backend.agents.agent_factory import AgentFactory
from backend.history.memory import ConversationMemory
from langchain.tools import tool
from langchain_core.messages import BaseMessage

class BillingAgent:

    def __init__(self,vectorstore):

        self.vectorstore = vectorstore
        self.agent_factory = AgentFactory()
        self.memory = ConversationMemory()
        
        retriever = self.vectorstore.get_retriever(
            categories=["pricing", "refund_policy", "shipping"]
        )

        @tool
        def billing_retriever(query: str) -> str:
            """
            Search billing-related knowledge base documents.
            """
            docs = retriever.invoke(query)

            return "\n\n".join(
                doc.page_content for doc in docs
            )

        self.tools = [billing_retriever]

        self.prompt = """
            You are TechMart's Billing Support Agent.

            Your responsibilities include:
            - Payment issues
            - Subscription queries
            - Billing errors
            - Refund status
            - Invoice requests

            Always search the knowledge base before answering.

            If the answer is not available in the retrieved documents,
            politely tell the customer that the information is unavailable.
            """

        self.agent = self.agent_factory.create_agent(
            tools=self.tools,
            system_prompt=self.prompt
        )

    def invoke_billingagent(
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