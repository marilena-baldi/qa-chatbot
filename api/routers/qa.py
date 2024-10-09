from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette import status

from api.schema.qa import QABase, QACreate, QARead, QAReadUD, QA
from db.repository.Repository import Repository
from db.controller.Controller import Controller
from db.database import SessionLocal
from api.dependencies import get_session, get_detail, get_cud_session
import db.model.qa

router = APIRouter(
    prefix="/qas",
    tags=['QAs']
)


@router.get("/", response_model=List[QA], status_code=status.HTTP_200_OK, responses={status.HTTP_404_NOT_FOUND: {}})
def get_qas(request: QARead = Depends(), session: SessionLocal = Depends(get_session)):
    qa_controller = Controller(Repository(session=session, table=db.model.qa.QA))
    qas = qa_controller.get(element=request)

    if not qas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return qas


@router.post("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response, responses={status.HTTP_409_CONFLICT: {}})
def create_qas(request: QACreate, session: SessionLocal = Depends(get_cud_session)):
    qa_controller = Controller(Repository(session=session, table=db.model.qa.QA))

    try:
        qa_controller.insert(element=request)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=get_detail(e))


@router.patch("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response, responses={status.HTTP_409_CONFLICT: {}, status.HTTP_404_NOT_FOUND: {}})
def update_qas(request_update: QABase, request: QAReadUD = Depends(), session: SessionLocal = Depends(get_cud_session)):
    qa_controller = Controller(Repository(session=session, table=db.model.qa.QA))

    try:
        qa_res = qa_controller.update(element_old=request, element_new=request_update)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=get_detail(e))

    if qa_res == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response, responses={status.HTTP_404_NOT_FOUND: {}})
def delete_qas(request: QAReadUD = Depends(), session: SessionLocal = Depends(get_cud_session)):
    qa_controller = Controller(Repository(session=session, table=db.model.qa.QA))
    qa_res = qa_controller.remove(element=request)

    if qa_res == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
