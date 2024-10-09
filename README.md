# QA chatbot

- [Description](#description)
- [Getting started](#getting-started)
- [Test](#test)
- [Future work](#future-work)
- [References](#references)


## Description
This project aims to provide the basic backend for a similarity based Q&A chatbot application.

Endpoints are divided in two routers: one to chat with the chatbot and one to add question-answer pairs in a postgresql database.

There is a web server with APIs (Uvicorn - FastAPI), which are validated thanks to the models (Pydantic) that map the data with an ORM toolkit (SQLAlchemy).

The project is organized as follows:
- The ai folder has:
  - a class AIModel that represents the AI model [[1]](#1) that embeds the sentences;
  - a class AIController that handles the user requests and uses the AI model to understand the most similar question in the database to return the corresponding answer;
- The api folder has:
  - the routers for the chatbot and the QAs pairs;
  - the pydantic schemas to validate requests and responses for the chat and the qas data;
- The db folder has:
  - the sqlalchemy model for the QA table;
  - the repository that handles the CRUD methods on the database data;
  - the controller that bridges the data operations exposed to the users with the APIs;
  - the database configuration file;
- The utils folder has:
  - a class Container used for dependency injection, to set and get the QAs and the AIModel;
  - a bootstrap file that has functions to initialize the database and the AI;


## Getting started

Create the .env file with the username, password and database name you want to create (or just leave it as the .env.dist).

You can change the container ports of the chatbot, postgres db and adminer services in the .env file or the host ports in the docker-compose.yaml. 

The latest (docker-compose.yaml) has two lines which are commented out that are responsible to make the database data persistent across runs. That's why there is a .dockerignore.

To get started place in the base project folder and just type:

```sh
make build  # to build all docker containers

make up  # to run the containers

make tail  # to tail on the webserver logs
```

Notice it may take a while to build and go up the first time because it will download the neural network model and some heavy machine learning library.

To stop the services, type:
```sh
make down
```

## Test

Once you run the system, you can test it with the api documentation. If you didn't change the containers ports:
- http://localhost:8888/docs to add question-answer pairs and test the chatbot;
- http://localhost:8886/adminer to access the database.

You can add the desired question-answer pairs making POST requests on the qas router and ask the chatbot to answer you using a chat GET on the chats router.

## Future work

In this version:
- the chat controller could use a lru caching mechanism to reduce latency due to getting updated with the database questions and answers;
- the endpoints that interact with the database could be improved to provide more useful information when conflicts happen.

## References
<a id="1">[1]</a> 
Nils Reimers and Iryna Gurevych (2019). 
Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks
https://arxiv.org/pdf/1908.10084.pdf