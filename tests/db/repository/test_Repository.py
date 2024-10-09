import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy_utils.functions import drop_database

from db.database import Base
from db.model.qa import QA
from db.repository.Repository import Repository


engine = create_engine(f'{os.environ.get("DBMS")}://{os.environ.get("DB_USER")}:'
                       f'{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}:'
                       f'{os.environ.get("DB_PORT")}/{os.environ.get("TEST_DB_NAME")}', echo=False,
                       poolclass=NullPool)

Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def init_db():
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)
    Base.metadata.create_all(engine)


def drop_db():
    if database_exists(engine.url):
        drop_database(engine.url)


class TestRepository(unittest.TestCase):

    def test_get_dict(self):
        qa_obj = QA(question='Question', answer='Answer')
        repository = Repository(session=Session(), table=QA)
        result = repository.get_dict(qa_obj)

        self.assertIsInstance(result, dict)

    def test_query(self):
        init_db()

        qa_obj = QA(question='Blue pill or red pill', answer='Yes')
        repository = Repository(session=Session(), table=QA)
        repository.create(qa_obj)
        result = repository.query(repository.get_dict(qa_obj))

        self.assertIsInstance(result, Query)

    def test_create(self):
        init_db()

        qa_obj = QA(question='What is the answer to life?', answer='42')
        repository = Repository(session=Session(), table=QA)
        result = repository.create(qa_obj)

        self.assertEqual(result, 1)

        drop_db()

    def test_read(self):
        init_db()

        qa_obj = QA(question='What is the number of the beast?', answer='666')
        repository = Repository(session=Session(), table=QA)
        repository.create(qa_obj)

        qa_id = QA(id=1)
        result = repository.read(qa_id)

        self.assertEqual(result[0].question, qa_obj.question)
        self.assertEqual(result[0].answer, qa_obj.answer)

        qa_question = QA(question=qa_obj.question)
        result = repository.read(qa_question)

        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].answer, qa_obj.answer)

        qa_answer = QA(answer=qa_obj.answer)
        result = repository.read(qa_answer)

        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].question, qa_obj.question)

        drop_db()

    def test_update(self):
        init_db()

        qa_obj = QA(question='What time is it?', answer='4:20')
        qa_obj_2 = QA(question='What is the time?', answer='4:21')

        session = Session()
        repository = Repository(session=session, table=QA)
        repository.create(qa_obj)
        repository.create(qa_obj_2)
        session.commit()

        qa_question = QA(question=qa_obj.question)
        qa_question_upd = QA(question=qa_obj_2.question)

        with self.assertRaises(IntegrityError):
            repository.update(qa_question, qa_question_upd)
        session.rollback()

        qa_answer = QA(answer=qa_obj.answer)
        qa_answer_upd = QA(answer=qa_obj_2.answer)
        result = repository.update(qa_answer, qa_answer_upd)

        self.assertEqual(result, 1)

        drop_db()

    def test_delete(self):
        init_db()

        qa_obj = QA(question='Should I stay or should I go now?', answer='If I go there will be trouble')

        repository = Repository(session=Session(), table=QA)

        qa_id = QA(id=1)
        result = repository.delete(qa_id)

        self.assertEqual(result, 0)

        repository.create(qa_obj)

        result = repository.delete(qa_id)

        self.assertEqual(result, 1)

        drop_db()
