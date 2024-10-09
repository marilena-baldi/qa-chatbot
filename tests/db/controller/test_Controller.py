import unittest

from db.controller.Controller import Controller
from db.model.qa import QA
from api.schema.qa import QACreate
from tests.mock.RepositoryMock import RepositoryMock

company_schema = QACreate(question="test question", answer="test answer")

controller = Controller(RepositoryMock(session=None, table=QA))


class TestController(unittest.TestCase):
    def test_get_object_by_schema(self):
        result = controller.get_object_by_schema(company_schema)

        self.assertIsInstance(result, QA)
