import asyncio
import uuid
from threading import Thread
import numpy as np
import time
import torch
from sentence_transformers import util
from utils.Container import Container


class AIController(Thread):
    """
    AIController is a thread that handles the communication with the AI Model.
    """

    def __init__(self, container: Container) -> None:
        """
        Initializes the AIController.
        """

        self.container = container
        self.input_queue = {}
        self.output_queue = {}

        self.ai_model = self.container.get_instance('ai_model')
        self.buffer_time = 0.1
        self.threshold = 0.55
        self.no_und_message = "Non ho capito. Puoi ripetere per favore?"

        self.db_embeddings = None
        self.db_answers = None
        self.db_qas = None
        self.update_qas()

        super().__init__()
        self.start()

    def update_qas(self):
        """ Update the QA-Pairs with the new ones from the database. """

        self.db_qas = self.container.get_instance('qas')
        questions = [qa.question.lower() for qa in self.db_qas]
        self.db_answers = [qa.answer for qa in self.db_qas]
        self.db_embeddings = self.ai_model.get_embeddings(questions=questions) if questions else None

    def enqueue(self, question: str) -> str:
        """
        Adds a question to the input queue.

        :param question: question to answer
        :type question: str
        :return: unique id of the request
        :rtype: str
        """

        unique_id = str(uuid.uuid4())
        self.input_queue[unique_id] = question.lower()

        return unique_id

    async def dequeue(self, unique_id: str) -> str:
        """
        Returns the answer of the request with the given unique id.

        :param unique_id: unique id of the request
        :type unique_id: str
        :return: answer of the question request
        :rtype: str
        """

        while unique_id not in self.output_queue:
            await asyncio.sleep(self.buffer_time/2)

        response = self.output_queue[unique_id]
        del self.output_queue[unique_id]

        return response

    def run(self) -> None:
        """
        Starts the AIController.
        """

        while True:
            if self.input_queue:
                self.update_qas()
                questions = list(self.input_queue.values())
                unique_ids = list(self.input_queue.keys())

                embeddings = self.ai_model.get_embeddings(questions=questions)
                for idx, embedding in enumerate(embeddings):
                    answer = self.no_und_message
                    if self.db_embeddings is not None:
                        sim = util.pytorch_cos_sim(a=torch.tensor(self.db_embeddings, device=self.ai_model.device), b=embedding)

                        if sim[np.argmax(sim.cpu())] > self.threshold:
                            answer = self.db_answers[np.argmax(sim.cpu())]

                    self.output_queue[unique_ids[idx]] = answer
                    del self.input_queue[unique_ids[idx]]

            time.sleep(self.buffer_time)
