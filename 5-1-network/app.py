# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Dict

# app = FastAPI()

# # 데이터 저장소 (임시 데이터베이스 역할)
# data_store: Dict[str, Dict] = {}

# class Data(BaseModel):
#     gi: str
#     team : str
#     role : str 
#     name : str  

# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to the FastAPI application!"}

# # 간단한 GET 요청에 대한 응답
# @app.get("/hello")
# async def hello_world():
#     return {"message": "Hello, World!"}


# # GET 요청으로 전체 데이터 목록 조회
# @app.get("/list")
# async def get_all_data():
#     return {"data": data_store}

# # GET 요청으로 데이터 조회
# @app.get("/data/{name}")
# async def get_data(name: str):
#     data = data_store.get(name)
#     if data is None:
#         raise HTTPException(status_code=404, detail="Data not found")
#     return {"data": data}

# # PUT 요청으로 데이터 수정
# @app.put("/list/{name}")
# async def update_data(name: str, data: Data):
#     if name not in data_store:
#         raise HTTPException(status_code=404, detail="Data not found")
#     data_store[name] = data.dict()
#     return {"status": "success", "updated_data": data}

# # DELETE 요청으로 데이터 삭제
# @app.delete("/list/{name}")
# async def delete_data(name: str):
#     if name not in data_store:
#         raise HTTPException(status_code=404, detail="Data not found")
#     del data_store[name]
#     return {"status": "success", "deleted_name": name}

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

# 브라우저에서 데이터를 넣고 빼봤습니당

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class Data(BaseModel):
    gi: str
    team: str
    role: str
    name: str

# 전역 데이터 저장소
data_store: List[Data] = []

# 귀찮으니깐 한번에...ㅎㅎ
@app.post("/list", response_model=List[Data])
def post_list():
    student_list = [
        Data(gi='23기', team='DE팀', role='전 부대장', name='이어흥'),
        Data(gi='24기', team='DE팀', role='팀장', name='임채림'),
        Data(gi='22기', team='DS팀', role='교육부장', name='김지훈'),
        Data(gi='24기', team='DE팀', role='부회장', name='조윤영'),
        Data(gi='24기', team='DS팀', role='회장', name='이동진')
    ]
    data_store.extend(student_list)
    return student_list

"""
@app.post("/list", response_model=Data)
def post_list(data: Data):
    data_store.append(data)
    return data
"""
    
@app.get("/list", response_model=List[Data])
def get_list():
    return data_store

@app.put("/list/{name}", response_model=Data)
def put_list(name: str, data: Data):
    for i, d in enumerate(data_store):
        if d.name == name:
            data_store[i] = data
            return data
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/list/{name}", response_model=Data)
def delete_list(name: str):
    for i, d in enumerate(data_store):
        if d.name == name:
            data_store.pop(i)
            return d
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, log_level="info")