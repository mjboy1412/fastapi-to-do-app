from peewee import *

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel as BaseSchema

import logging

logger = logging.getLogger("peewee")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

db = SqliteDatabase("my_database.db")


class BaseModel(Model):
    class Meta:
        database = db


class Todo(BaseModel):
    name = TextField()
    completed = BooleanField()

    def to_dict(self):
        return vars(self)["__data__"]


db.connect()
db.create_tables([Todo])

app = FastAPI()


class TodoSchema(BaseSchema):
    name: str
    completed: bool


@app.get("/todos")
def get_all_todo():
    query = Todo.select().dicts()
    todos = [e for e in query]
    return {"todos": todos}


@app.get("/todo/{todo_id}")
def get_a_todo(todo_id: int):
    query_read_todo = Todo.get_or_none(todo_id)
    if query_read_todo == None:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    else:
        result = query_read_todo.to_dict()
        return {"updated todo at": result}


@app.post("/todos/create")
def create_a_todo(todo: TodoSchema):
    result = Todo.create(name=todo.name, completed=todo.completed)
    return {"todo": result.to_dict()}


@app.put("/todo/{todo_id}")
def update_todo(todo_id: int, todo: TodoSchema):
    query_read_todo = Todo.get_or_none(todo_id)
    if query_read_todo == None:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    else:
        query_update = Todo.update(
            {Todo.name: todo.name, Todo.completed: todo.completed}
        ).where(Todo.id == todo_id)
        result = query_update.execute()
        return {"updated todo at": result}


@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    query_read_todo = Todo.get_or_none(todo_id)
    if query_read_todo == None:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    else:
        query_delete = Todo.delete().where(Todo.id == todo_id)
        result = query_delete.execute()
        return {"delete todo at": result}
