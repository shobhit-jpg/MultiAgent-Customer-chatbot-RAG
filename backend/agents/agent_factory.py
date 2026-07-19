import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent


class AgentFactory:

    def __init__(self):
        self.api = os.environ.get("GROQ_API_KEY")
        self.llm = ChatGroq(
            api_key=self.api,
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_retries=2,
            verbose=True
        )

    def create_agent(self, tools, system_prompt: str):

        agent = create_agent(
            model=self.llm,
            tools=tools,
            system_prompt=system_prompt
        )

        return agent