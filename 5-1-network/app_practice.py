from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI() # 애플리케이션 인스턴스 생성 

# 데이터 저장소 (임시 데이터베이스 역할)
data_store: Dict[str, Dict] = {}
# 메모리 내 데이터 저장소로 사용될 빈 딕셔너를 지정 > 데이터의 이름을 키로 사용하여 데이터 저장 

class Data(BaseModel):
    name: str
    age: int

@app.get("/") # 메인페이지 
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# 간단한 GET 요청에 대한 응답 
@app.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}

# raise 구문 에러를 일부로 발생시키는 
# POST 요청을 받아 JSON 응답을 반환
@app.post("/data", status_code=201) # async 비동기 함수 > 입출력 작업을 효율적으로 처리 가능 
async def receive_data(data: Data): # data : 사용자가 입력한 데이터 , Data : 내가 위해서 지정한 모델 이고 자동으로 타입이 맞는지 확인함 즉 유효성 검사 구문  
    if data.name in data_store:  # data_store 위에 지정해둠 
        raise HTTPException(status_code=400, detail="Data with this name already exists")
    data_store[data.name] = data.dict() # data_store에 없다면 data 객체를 딕셔너리로 변환하여 data_store 저장 , data.dict pydantic 모델 인스턴스를 딕셔너리로 변환하는 메서드 
    return {"status": "success", "name": data.name, "received_data": data} # 성공적으로 저장되면 상태 메시지와 저장된 데이터를 변환 

# GET 요청으로 전체 데이터 목록 조회
@app.get("/data")
async def get_all_data():
    return {"data": data_store}

# GET 요청으로 데이터 조회
@app.get("/data/{name}")
async def get_data(name: str):
    data = data_store.get(name) # 키 값을 가져오는 거임 
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"data": data} # 데이터가 있다면 name 대신 > data가 키 값이 됨 

# PUT 요청으로 데이터 수정
@app.put("/data/{name}") # 경로 파라미터 
async def update_data(name: str, data: Data): # Data는 단순한 타입 힌트 이상의 역할 validation 까지 됨
    if name not in data_store:
        raise HTTPException(status_code=404, detail="Data not found")
    data_store[name] = data.dict() # 맞는 키에 접근하여 데이터를 업데이트 하는, data.dict data 객체를 딕셔너리로 변환하여 name 키에 저장 data.dict 메서드는  모델 인스턴스를 딕셔너리로 변환 
    return {"status": "success", "updated_data": data}

# DELETE 요청으로 데이터 삭제
@app.delete("/data/{name}") 
async def delete_data(name: str):
    if name not in data_store:
        raise HTTPException(status_code=404, detail="Data not found")
    del data_store[name]
    return {"status": "success", "deleted_name": name} # name 을 사용할 수 있는 이유 > 값이 아니라 파라미터 이기 때문에

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    # uvicorn > 실행하는데 사용하고 여러 매개변수를 받아 서버의 동작 방식 설명 
    # app > 애플리케이션 인스턴스 
    # host > 서버가 바인딩할 ip 주소  127.0.0.1 로컬 호스트 
    # port > 서버가 바인딩할 포트 
    # log > 로그 레벨 지정 info > 정보 레벨의 로그를 출력하도록 설정 error,debug,warning 등이 있음 