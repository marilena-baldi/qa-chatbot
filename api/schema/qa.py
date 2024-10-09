from typing import Optional
from pydantic import BaseModel, root_validator

from api.schema.validators import validate_any_of


class QABase(BaseModel):
    """ Base schema to validate the QA data. """

    question: Optional[str] = None
    answer: Optional[str] = None

    _check_values = root_validator(allow_reuse=True)(validate_any_of)


class QACreate(QABase):
    """ Schema to validate the QA data for create operations. """

    question: str
    answer: str


class QARead(BaseModel):
    """ Schema to validate the QA data for read operations. """

    id: Optional[int] = None


class QAReadUD(BaseModel):
    """ Schema to validate the QA data for read in update and delete operations. """

    id: int


class QA(BaseModel):
    """ Schema to validate the QA data. """

    id: int
    question: str
    answer: str

    class Config:
        orm_mode = True
