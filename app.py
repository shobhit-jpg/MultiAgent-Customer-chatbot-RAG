import warnings

warnings.filterwarnings("ignore")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from backend.history.memory import ConversationMemory
from backend.agents.intent_detector import IntentAgent
from backend.agents.billing_agent import BillingAgent
from backend.agents.technical_agent import TechnicalAgent
from backend.agents.products_agent import ProductsAgent
from backend.agents.faq_agent import FaqAgent
from backend.agents.complaint_agent import ComplaintAgent
from backend.rag.create_db import CreateDb



app = FastAPI(title="TechMart Customer Care API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_creator = CreateDb()
vectorstore = db_creator.build_vectorstore()


memory = ConversationMemory()
intent_agent = IntentAgent()
billing_agent = BillingAgent(vectorstore)
technical_agent = TechnicalAgent(vectorstore)
product_agent = ProductsAgent(vectorstore)
faq_agent = FaqAgent(vectorstore)
complaint_agent = ComplaintAgent()

class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.post("/new-chat")
def new_chat():

    session = memory.new_chat()
    print("NEW SESSION CREATED:", session)
    return {
        "session_id": session
    }


@app.post("/chat")
def chat(request: ChatRequest):

    query = request.message
    session = request.session_id
    intent = intent_agent.detect_intent(query,session_id = session)
    print(intent)

    if intent == "billing":

        reply = billing_agent.invoke_billingagent(query, session)

    elif intent == "technical":

        reply = technical_agent.invoke(query, session)

    elif intent == "product":

        reply = product_agent.invoke(query, session)

    elif intent == "faq":

        reply = faq_agent.invoke(query, session)

    elif intent == "complaint":

        reply = complaint_agent.invoke(query, session)  

    elif intent == "escalate":
        print("Escalate")
        intent == "escalate"
        reply = "Sorry, I couldn't understand your request Connecting you to a Techmart agent for better support ."

    else:
        print("no intent")
        intent == "unidentified"
        reply = "Sorry, I couldn't understand your request Connecting you to a Techmart agent for better support "

    return {
        "intent": intent,
        "response": reply
    }


@app.get("/sessions")
def sessions():

    return memory.list_chats()


@app.get("/chat/{session_id}")
def history(session_id: str):

    return memory.get_chat(session_id)


@app.delete("/chat/{session_id}")
def delete(session_id: str):

    memory.delete_chat(session_id)

    return {
        "message": "Conversation deleted."
    }

app.mount(
    "/",
    StaticFiles(directory="frontend/dist", html=True),
    name="frontend"
)