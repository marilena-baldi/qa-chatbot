import os
from typing import List, Union

import torch
from sentence_transformers import SentenceTransformer


class AIModel:
    def __init__(self) -> None:
        """
        Initialize the model.
        """

        self.device = 'cuda:0' if os.environ.get('DEVICE') == 'gpu' else 'cpu'
        model_folder = os.path.join('ai', 'data', 'paraphrase-multilingual-mpnet-base-v2')

        self.model = SentenceTransformer(model_name_or_path='paraphrase-multilingual-mpnet-base-v2',
                                            device=self.device,
                                            cache_folder=os.path.split(model_folder)[0])
        if self.device == 'cpu':
            self.model = torch.quantization.quantize_dynamic(self.model, {torch.nn.Linear}, dtype=torch.qint8)

    def get_embeddings(self, questions: List[str]) -> Union[List[torch.Tensor], torch.Tensor]:
        """
        Get the embeddings for the given questions.

        :param questions: questions to get embeddings for
        :type questions: List[str]
        :return: embeddings for the given questions
        :rtype: torch.Tensor
        """

        embeddings = self.model.encode(sentences=questions, convert_to_tensor=True, device=self.device)

        return embeddings
