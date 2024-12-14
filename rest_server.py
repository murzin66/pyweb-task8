from fastapi import FastAPI, HTTPException
from grpc import insecure_channel
import grpc
import dictionary_pb2
import dictionary_pb2_grpc
from pydantic import BaseModel
from typing import List
import os
from google.protobuf.empty_pb2 import Empty

# Подключение к gRPC серверу
grpc_host = os.getenv("GRPC_SERVER_HOST", "grpc-server")
grpc_port = os.getenv("GRPC_SERVER_PORT", "50051")

channel = insecure_channel(f"{grpc_host}:{grpc_port}")
stub = dictionary_pb2_grpc.DictionaryServiceStub(channel)

# Создание FastAPI приложения
app = FastAPI()

# Pydantic модели для запросов и ответов
class Term(BaseModel):
    id: int
    term: str
    definition: str
    priority: int

class TermsList(BaseModel):
    terms: List[Term]

class AddTermRequest(BaseModel):
    term: Term

class AddTermResponse(BaseModel):
    message: str

class GetTermRequest(BaseModel):
    term: str

class GetTermResponse(BaseModel):
    term: Term

@app.post("/terms", response_model=AddTermResponse)
async def add_term(term: AddTermRequest):
    # Преобразуем Pydantic модель в gRPC запрос
    grpc_term = dictionary_pb2.Term(
        term=term.term.term,
        definition=term.term.definition,
        priority=term.term.priority
    )
    response = stub.AddTerm(dictionary_pb2.AddTermRequest(term=grpc_term))
    return AddTermResponse(message=response.message)

@app.get("/terms", response_model=TermsList)
async def get_all_terms():
    response = stub.GetAllTerms(Empty())
    terms = [Term(id=term.id, term=term.term, definition=term.definition, priority=term.priority) for term in response.terms]
    return TermsList(terms=terms)

@app.get("/term/{term_name}", response_model=GetTermResponse)
async def get_term(term_name: str):
    grpc_response = stub.GetTerm(dictionary_pb2.GetTermRequest(term=term_name))
    if grpc_response.term:
        term = grpc_response.term
        return GetTermResponse(term=Term(id=term.id, term=term.term, definition=term.definition, priority=term.priority))
    raise HTTPException(status_code=404, detail="Term not found")

@app.put("/terms", response_model=AddTermResponse)
async def update_term(term: AddTermRequest):
    try:
        grpc_term = dictionary_pb2.Term(
            id=term.term.id,  # Добавлен ID
            term=term.term.term,
            definition=term.term.definition,
            priority=term.term.priority
        )
        response = stub.UpdateTerm(dictionary_pb2.UpdateTermRequest(term=grpc_term))
        return AddTermResponse(message=response.message)
    except grpc.RpcError as e:
        raise HTTPException(status_code=404 if e.code() == grpc.StatusCode.NOT_FOUND else 500, detail=e.details())

@app.delete("/term/{term_id}", response_model=AddTermResponse)
async def delete_term(term_id: int):
    try:
        response = stub.DeleteTerm(dictionary_pb2.DeleteTermRequest(id=term_id))  # Передаем ID
        return AddTermResponse(message=response.message)
    except grpc.RpcError as e:
        raise HTTPException(status_code=404 if e.code() == grpc.StatusCode.NOT_FOUND else 500, detail=e.details())
