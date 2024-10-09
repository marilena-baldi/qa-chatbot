import pytest

from api.schema.chatbot import ChatRequest
from db.controller.Controller import Controller
from db.database import SessionLocal
from db.model.qa import QA
from db.repository.Repository import Repository
from utils.Container import Container
from tests.mock.AIModelMock import AIModelMock
from ai.controller.AIController import AIController


container = Container()
chat_request = ChatRequest(question="What is the capital of Italy?")

container.set_instance('ai_model', AIModelMock(None))
question_controller = Controller(Repository(session=SessionLocal(), table=QA))
qas = question_controller.get()
container.set_instance('qas', qas)
ai_controller = AIController(container=container)
uuids = []


class TestAIController:
    def test_enqueue(self):
        assert len(ai_controller.input_queue) == 0

        uuid = ai_controller.enqueue(question=chat_request.question)
        uuids.append(uuid)

        assert len(ai_controller.input_queue) == 1

    @pytest.mark.asyncio()
    async def test_dequeue(self):

        assert len(ai_controller.input_queue) == 1

        await ai_controller.dequeue(unique_id=uuids[0])

        assert len(ai_controller.input_queue) == 0
