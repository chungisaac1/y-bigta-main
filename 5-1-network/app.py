# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Dict

# app = FastAPI()

# # 데이터 저장소 (임시 데이터베이스 역할)
# data_store: Dict[str, Dict] = {}

# class Data(BaseModel):
#     gi: str
#     team: str
#     role : str 
#     name : str 


# # POST 요청을 받아 JSON 응답을 반환
# @app.post("/list", status_code=201)
# async def receive_data(data: Data):
#     if data.name in data_store:
#         raise HTTPException(status_code=400, detail="Data with this name already exists")
#     data_store[data.name] = data.dict()
#     return {"status": "success", "name": data.name, "received_data": data}

# # GET 요청으로 전체 데이터 목록 조회
# @app.get("/list")
# async def get_all_data():
#     return {"data": data_store}



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
#     # uvicorn 5-1-network.app:app --reload
# 저는 위에 걸로 하고 브라우저에서 추가하는 형태로 했습니다


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
data_store: List[Data] = [] # 위에서는 키 를 name 으로 접근했는데 여기서는 그냥 리스트로 했네 

# 귀찮으니깐 한번에...ㅎㅎ
@app.post("/list", response_model=List[Data]) # response > 엔드포인트 함수가 반환하는 응답의 데이터 모델 지정 자동으로 검증하고 직렬화 list[data] 는 타입 힌트  
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

# enumerate > iterable 와 함께 사용되어 각 요소와 그 요소의 인덱스를 함께 반환하는 각 요소의 인덱스와 값을 동시에 사용할 수 있음
@app.put("/list/{name}", response_model=Data) # name 에는 기본 이름 data 에는 new 이름 
def put_list(name: str, data: Data):
    for i, d in enumerate(data_store):
        if d.name == name:
            data_store[i] = data # 그 인덱스에 넣어라 데이터를  
            return data
    raise HTTPException(status_code=404, detail="Item not found")

# del 
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