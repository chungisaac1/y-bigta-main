import os
import sys
import pickle

# sys.path 는 파이썬 모듈 검색 경로 리스트 
# 목적 > 스크립트가 어디서 실행되든지 간에 항상 현재 스크립트가 위치한 디렉토리 안에 version 파일을 생성하고 사용하기 위함  
# 다른 디렉토리에서 스크립트를 하더라도 일관되게 디렉토리에 저장되도록 
PICKLE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/versions.pickle"
# pickle_path > pickle 모듈을 사용해 데이터 , 직- 역직 한 데이터를 저장하거나 불러올 파일의 경로 설정 
# pickle > 데이터 직,역직 함 > pickle_path > 직렬화된 데이터를 저장할 파일의 경로 지정 변수 
# __file__ > 현재 실행 중인 파이썬 스크립트의 파일 이름을 나타내는 내장 변수 
# os.path.abspath > 현재 스크립트의 절대 경로 반환 
# dirname > 스크립트의 절대 경로에서 디렉토리 부분만 출력 
# version > 뒤에 파일명 덧붙임  
# 결론 : 다른 곳에서도 사용할 수 있게 절대 경로 뽑아내기 
# pickle 모듈을 이용할 때 (데이터 저장,가져올 때) 디렉토리 뽑아내고 뒤에 문자열 넣기 자동으로 그래서 다른 곳에서도 저 경로로 파일을 이용할 수 있게 맞나?
def load() -> dict[str, list[str]]: # 키 str 타입의 문자열 , 값 list안에 str
    try:
        return pickle.load(open(PICKLE_PATH, "rb")) # 바이너리 읽기 ? 데이터를 바이트 단위로 읽을 수 있음 
        # versions.piickle 파일에서 데이터를 불러옴 
    except:
        return dict()
        # 파일 없거나 로드 실패하면 빈 딕셔너리 반환 

def vis(d: dict[str, list[str]]) -> str: # 딕셔너리 받아서 문자열 형식으로 변환
    s = [] # # items 딕셔너리의 키-값 상을 가져오는 메서드 > 튜플로 묶음  
    for k, v in d.items(): # k는 딕셔너리 키 값 , v는 딕셔너리 value 값 
        s.append(f"{k}") # k를 리스트에 추가 
        for path in v: # 2중 for문 
            s.append(f"    - {path}") #  앞에 띄어쓰기를 머금은 채 저장 하기 리스트 형태로 딕셔너리 아님 
    return "\n".join(s) # 구분자를 통해 리스트에 구분을 대체하고 문자열 출력 


if __name__ == "__main__":
    d = load() # version 파일에서 데이터 읽어서 딕셔너리 형태로 변환, 없으면 빈 딕셔너리 반환 
    d[sys.version] = sys.path # 딕셔너리니까 sys.version(현재 파이썬 버전) 키 에 value는 sys.path(모듈을 찾는데 사용되는 경로들의 리스트)

    print(f"current: {len(d)}\ndict:\n{vis(d)}") # len d > 딕셔너리에 저장된 파이썬 버전의 개수 , vis > 딕셔너리 내용을 보기 좋게 
    if len(d) >= 3:
        print("good!")

    pickle.dump(d, open(PICKLE_PATH, "wb"))
    # dump 파이썬 객체를 직렬화 하여 저장 
    # d는 직렬화할 파이썬 객체 , 파일을 바이너리 쓰기 모드로 열고, pickle_path 경로에 해당 파일 객체 반환 
    # wb > 파일이 존재하면 덮어쓰고 없으면 새 파일 만든다 
    # 바이너리 형식 > 데이터를 바이트 단위로 저장 , 인코딩 없음 
    # 바이너리 형식은 서버끼리 데이터를 주고 받을 때 , 일반적인 텍스트 저장과는 다름 