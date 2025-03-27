# FastAPI 백엔드 서버를 설정하는 메인 파일
'''
**백엔드 구현 (main.py)**

FastAPI를 활용해 CRUD(Create, Read, Update, Delete) 엔드포인트를 제공하고, Pydantic 모델(`TodoItem`)을 이용해 데이터의 구조를 정의함

각 엔드포인트(`GET`, `POST`, `PUT`, `DELETE`)에서 `todo.json` 파일을 읽고 쓰는 방식으로 데이터를 관리

루트 엔드포인트(`/`)에서는 HTML 파일을 읽어 브라우저에 서빙
'''

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import json
import os
from datetime import datetime

app = FastAPI()

# To-Do 항목 모델
class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    due_date: Optional[str] = None

# JSON 파일 경로
TODO_FILE = "todo.json"

# 프로그램 시작 시, to-do 항목 리셋
def reset_todo():
        default_data = []
        with open(TODO_FILE, "w",encoding="utf-8") as file:
                json.dump(default_data, file, indent=4)
    
# JSON 파일에서 To-Do 항목 로드
def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r",encoding="utf-8") as file:
            return json.load(file)
    return []

# JSON 파일에 To-Do 항목 저장
def save_todos(todos):
    with open(TODO_FILE, "w",encoding="utf-8") as file:
        json.dump(todos, file, indent=4)

# 날짜를 기준으로 todo를 정렬하는 함수
def sort_todos_by_date(todos, ascending=True):
    # 날짜가 없는 todo는 맨 뒤로 보내는 함수
    def get_date_or_max(todo):
        if not todo.get("due_date"):
            return "9999-12-31" if ascending else ""
        return todo["due_date"]
    return sorted(todos, key=get_date_or_max, reverse=not ascending)

# FastAPI 앱 시작 시 json 파일 초기화
@app.on_event("startup")
def startup_event():
    reset_todo()

# To-Do 목록 조회
@app.get("/todos", response_model=list[TodoItem])
def get_todos(sort_by_date: bool = Query(False), ascending: bool = Query(True)):
    todos = load_todos()
    if sort_by_date:
        todos = sort_todos_by_date(todos, ascending)
    return todos

# 신규 To-Do 항목 추가
@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoItem):
    todos = load_todos()
    todos.append(todo.dict())
    save_todos(todos)
    return todo

# To-Do 항목 수정
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo.update(updated_todo.dict())
            save_todos(todos)
            return updated_todo
    raise HTTPException(status_code=404, detail="To-Do item not found")

# To-Do 항목 삭제
@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int):
    todos = load_todos()
    todos = [todo for todo in todos if todo["id"] != todo_id]
    save_todos(todos)
    return {"message": "To-Do item deleted"}

# 특정 to-do 항목의 완료 여부 변경
@app.put("/todos/{todo_id}/complete", response_model=TodoItem)
def toggle_complete(todo_id: int):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"]=not todo["completed"]
            save_todos(todos)
            return todo
    raise HTTPException(status_code=404, detail="To-Do item not found")

# HTML 파일 서빙
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)
