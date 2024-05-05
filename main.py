import uuid
import json
import os
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from scheduler import start

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def queue_tt(id, data):
    contents = str(start(data))
    # create file id.txt
    with open(f"{id}.txt", "w") as f:
        f.write(contents)


@app.get("/")
def read_root():
    return {"success": "Houston, we are go for launch!"}


@app.post("/tt/new")
async def create(request: Request, background_tasks: BackgroundTasks):
    data = await request.body()
    print(data)
    data = json.loads(data)
    id = uuid.uuid4()
    background_tasks.add_task(queue_tt, id, data["data"])
    return {"success": str(id)}


@app.get("/tt/status/{id}")
def status(id):
    if not os.path.exists(f"{id}.txt"):
        return {"status": "processing"}
    with open(f"{id}.txt", "r") as f:
        return {"status": str(f.read())}
