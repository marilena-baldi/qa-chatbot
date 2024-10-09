FROM python:3.7-buster AS base
WORKDIR /chatbot
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
FROM base AS gpu
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu11
FROM base AS cpu
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
