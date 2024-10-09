from fastapi import APIRouter, Depends

from ai.controller.AIController import AIController
from api.schema.chatbot import InitResponse, ChatResponse, ChatRequest, InitRequest
from utils.Container import container

ai_controller = AIController(container=container)

router = APIRouter(
    prefix="/chats",
    tags=['Chats']
)


@router.get("/init", response_model=InitResponse)
async def init(request: InitRequest = Depends()):
    answer = "Ciao {}!".format(request.name)
    return InitResponse(answer=answer)


@router.get("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest = Depends()):
    unique_id = ai_controller.enqueue(question=request.question)
    response = await ai_controller.dequeue(unique_id=unique_id)
    return ChatResponse(answer=response)
