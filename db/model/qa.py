from sqlalchemy import Column, BigInteger, String, Sequence, UniqueConstraint

from db.database import Base


class QA(Base):
    """ Question&Answer model. """

    __tablename__ = 'qa'

    id = Column(BigInteger, Sequence('qa_id_seq'), primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('question', name='_qa_question_uc'),
                      )
