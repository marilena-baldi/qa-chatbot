from db.database import SessionLocal
from sqlalchemy_utils.types.pg_composite import psycopg2

from utils.bootstrap import update_qas_ref


def get_detail(e):
    """ Set the message for the integrity error. """

    if type(e.orig) is psycopg2.errors.ForeignKeyViolation:
        message = "La risorsa di riferimento non esiste."

    elif type(e.orig) is psycopg2.errors.UniqueViolation:
        message = "La risorsa esiste già."

    else:
        message = "Errore."

    return message


def get_session():
    session = SessionLocal()
    try:
        yield session

    except Exception:
        session.rollback()
        session.close()
        raise
    finally:
        session.commit()
        session.close()


def get_cud_session():
    session = SessionLocal()
    try:
        yield session

    except Exception:
        session.rollback()
        session.close()
        raise
    finally:
        session.commit()
        session.close()
        update_qas_ref()
