from pydantic import BaseModel


class InitRequest(BaseModel):
    """ Request schema for initializing the chatbot. """

    name: str


class InitResponse(BaseModel):
    """ Response schema for initializing the chatbot. """

    answer: str


class ChatRequest(BaseModel):
    """ Request schema for chatting with the chatbot. """

    question: str


class ChatResponse(BaseModel):
    """ Response schema for chatting with the chatbot. """

    answer: str
