from backend.agents.agent_factory import AgentFactory
from backend.history.memory import ConversationMemory
from backend.history.ComplaintManager import ComplaintManager
from langchain.tools import tool


class ComplaintAgent:

    def __init__(self):

        self.agent_factory = AgentFactory()
        self.complaint = ComplaintManager()
        self.memory = ConversationMemory()

        @tool
        def create_complaint(email :str ,subject :str ) -> dict:
                """
                    Create a new customer complaint.

                    Args:
                        email: Customer's email address.
                        subject: A short description of the complaint.

                    Returns:
                        A dictionary containing:
                        - success (bool)
                        - message (str)
                        - complaint_id (str)
                """
                result = self.complaint.create_complaint(email=email,subject=subject)
                return result
            
        self.tools = [create_complaint]

        self.prompt = """
            You are TechMart's Complaint Support Agent.

            Your responsibilities:
            - Help customers register complaints.
            - Ask for the customer's email if it is not provided.
            - Ask for a short subject describing the issue if it is not provided.
            - Once you have both the email and subject, call the create_complaint tool.
            - If the tool reports an existing open complaint, inform the customer and provide the complaint ID.
            - If a new complaint is created, provide the complaint ID and ask the customer to keep it for future reference.
            - Do not call the create_complaint tool until both the customer's email and the complaint subject have been collected.
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