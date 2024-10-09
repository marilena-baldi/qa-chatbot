import torch


class AIModelMock:
    def __init__(self, model):
        pass

    def get_embeddings(self, questions):
        return torch.ones((len(questions), 300))
