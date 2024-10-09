from sqlalchemy_utils import create_database, database_exists

from ai.model.AIModel import AIModel
from db.database import engine, SessionLocal, Base
from db.model.qa import QA
from db.controller.Controller import Controller
from db.repository.Repository import Repository
from ai.controller.AIController import AIController
from utils.Container import container


def update_qas_ref() -> None:
    """
    Update the database qas in the container.
    """

    session = SessionLocal()
    question_controller = Controller(Repository(session=session, table=QA))
    qas = question_controller.get()
    container.set_instance('qas', qas)
    session.close()


def init_ai() -> None:
    """
    Initialize the AI controller.

    :return: The initialized AI controller.
    :rtype: AIController
    """

    update_qas_ref()
    container.set_instance('ai_model', AIModel())


def init_db() -> None:
    """ Initialize the database. """

    session = SessionLocal()
    create_db()
    session.close()


def create_db() -> None:
    """ Create the database. """

    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
