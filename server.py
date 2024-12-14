import grpc
from concurrent import futures
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from google.protobuf.empty_pb2 import Empty

import dictionary_pb2
import dictionary_pb2_grpc

# Database setup
DATABASE_URL = "sqlite:///db/terms.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TermModel(Base):
    __tablename__ = "terms"
    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, unique=True, index=True)
    definition = Column(String)
    priority = Column(Integer)


Base.metadata.create_all(bind=engine)


initial_terms = [
            {"term": "Система управления обучением (LMS)", "definition": "Платформа или программное обеспечение для интеграции инструментов обучения", "priority": 1},
            {"term": "Граф знаний", "definition": "Коллекция взаимосвязанных сущностей и их описаний", "priority": 2},
            {"term": "Онтология", "definition": "Семантическая модель данных, описывающая сущности реального мира", "priority": 3},
            {"term": "Стемминг", "definition": "Поиск формы слова, учитывающий морфологию исходного слова", "priority": 4},
            {"term": "Индуктивные методы заполнения графа знаний", "definition": "Методы предсказания отсутствующих триплетов между новыми сущностями", "priority":5},
            {"term": "Дедуктивные методы заполнения графа знаний", "definition": "Методы, основанные на сопоставлении сущностей и отношений между ними с помощью формальных правил", "priority":6},
            {"term": "Гетерогенный граф", "definition": "Граф с различными типами узлов и рёбер", "priority": 7},
            {"term": "Граф свойств", "definition": "Тип графовой модели, в которой отношения имеют имя и свойства", "priority": 8},
            {"term": "Семантическая схема", "definition": "Схема, определяющая значение высокоуровневых терминов и иерархию классов", "priority": 9},
            {"term": "Валидирующая схема", "definition": "Схема, описывающая минимальный набор данных для обеспечения полноты графа знаний", "priority": 10},
            {"term": "Эмерджентная схема", "definition": "Схема, описывающая скрытые структуры графа знаний", "priority": 11},
            {"term": "Ризонинг", "definition": "Технология выявления новых связей между сущностями в графе знаний", "priority": 12},
            {"term": "Эмбеддинг", "definition": "Векторное представление сущностей графа знаний и отношений между ними", "priority": 13},
            {"term": "GraphQL", "definition": "Язык запросов к API и среда выполнения для выполнения этих запросов", "priority": 14},
            {"term": "REST", "definition": "Архитектурный стиль для разработки веб-сервисов и систем", "priority": 15},
            {"term": "DBpedia", "definition": "Проект по извлечению структурированного контента из Википедии", "priority": 16},

]


def init_db():
    db = SessionLocal()
    for term in initial_terms:
        if not db.query(TermModel).filter(TermModel.term == term["term"]).first():
            db.add(TermModel(**term))
    db.commit()
    db.close()


class DictionaryService(dictionary_pb2_grpc.DictionaryServiceServicer):
    def GetAllTerms(self, request, context):
        db = SessionLocal()
        terms = db.query(TermModel).all()
        db.close()
        return dictionary_pb2.TermsList(
            terms=[dictionary_pb2.Term(id=t.id, term=t.term, definition=t.definition, priority=t.priority) for t in terms]
        )

    def GetTerm(self, request, context):
        db = SessionLocal()
        term = db.query(TermModel).filter(TermModel.term == request.term).first()
        db.close()
        if term:
            return dictionary_pb2.GetTermResponse(
                term=dictionary_pb2.Term(id=term.id, term=term.term, definition=term.definition, priority=term.priority)
            )
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Term not found")
        return dictionary_pb2.GetTermResponse()

    def AddTerm(self, request, context):
        db = SessionLocal()
        new_term = TermModel(
            term=request.term.term,
            definition=request.term.definition,
            priority=request.term.priority,
        )
        db.add(new_term)
        db.commit()
        db.close()
        return dictionary_pb2.AddTermResponse(message="Term added successfully!")

    def UpdateTerm(self, request, context):
        db = SessionLocal()
        term = db.query(TermModel).filter(TermModel.id == request.term.id).first()
        if term:
            term.term = request.term.term
            term.definition = request.term.definition
            term.priority = request.term.priority
            db.commit()
            db.close()
            return dictionary_pb2.UpdateTermResponse(message="Term updated successfully!")
        db.close()
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Term not found")
        return dictionary_pb2.UpdateTermResponse(message="Term not found")

    def DeleteTerm(self, request, context):
        db = SessionLocal()
        term = db.query(TermModel).filter(TermModel.id == request.id).first()  # Удаляем по ID
        if term:
            db.delete(term)
            db.commit()
            db.close()
            return dictionary_pb2.DeleteTermResponse(message="Term deleted successfully!")
        db.close()
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Term not found")
        return dictionary_pb2.DeleteTermResponse(message="Term not found")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dictionary_pb2_grpc.add_DictionaryServiceServicer_to_server(DictionaryService(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server is running on port 50051")
    init_db()
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
