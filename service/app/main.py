# service/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from .db import get_db, init_db

app = FastAPI(title="mini-cloud-service")

class ItemIn(BaseModel):
    name: str

class ItemOut(BaseModel):
    id: int
    name: str

@app.on_event("startup")
async def startup():
    init_db()  # создаст таблицу если нет

@app.get("/items", response_model=List[ItemOut])
def list_items():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    return [{"id": r[0], "name": r[1]} for r in rows]

@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(item: ItemIn):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO items(name) VALUES (%s) RETURNING id", (item.name,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return {"id": new_id, "name": item.name}

@app.get("/healthz")
def health():
    return {"status": "ok"}
