from lib import Matrix
from typing import Callable
import sys


"""
아무것도 수정하지 마세요!
"""

# 헷갈린게 intify가 int로 바꿔주는 건 알겠는데 int로만 바꿔주는지 아니면 int로 바꿔주고 리스트도 하나 더 생성하는 건지 
# 답은 int로 만 바꿔주고 그 값을 list 에 저장하는겅미 그 안에 2차원 배열을 만드는게 아니라 

def main() -> None:
    intify: Callable[[str], list[int]] = lambda l: [*map(int, l.split())] # > 이 함수는 입력을 받으면 공백을 기준으로 나누고 int 로 바꾼다 
    # intify 라는 변수에 lambda 함수 넣기 callable 은 설명 str> list[int] 결과물 
    # map 첫 번째 인자로 받은 함수를 두 번째 인자를 변환하는 객체로 만듬 
    # *map 은 객체의 모든 요소를 즉시 리스트로 변호나 > list(map(int,)) 이거랑 같음 
    lines: list[str] = sys.stdin.readlines()
    # list[str] 은 그냥 명시용 
    # sys.stdin.readlines() > 줄 바꿈으로 나눠서 입력을 받고 그걸 리스트로 바로 반환해줌 > 개사기 

    N, B = intify(lines[0]) # > 첫번째 값을 int로 바꿈 
    matrix: list[list[int]] = [*map(intify, lines[1:])] # intify 적용하고 lines 에 0번째 값 제외하고 실행 리스트로 감 쌈 
    # split() 공백으로 나누는데 3 5 > 3,5 이렇게 해줌 근데 sys 하면 사실 3 5 가 아니라 3 5|n임 그래서 split() 이 끝남 
    # 그래서 for 문으로 돌리는거 한 줄 한 줄 다음주 개념으로 


    Matrix.MOD = 1000 # Matrix 클래스 안에 MOD 라는 속성을 1000 으로 설정 
    modmat = Matrix(matrix) # martix 라는 데이터를 사용하여 Martrix 클래스의 인스턴스를 생성하는거 
    #Martix 라는 클래스가 있고 matrix로 그 값을 던지는거지 그러면 그 안에 여러 함수들을 적용 시킬 수 있고 
    # matrix 라는 변수 안에는 intify , lines 라는 함수가 있고 그걸 실행 시켜주는 martix라는 본체가 있는거네 
    print(modmat ** B) # b는 몇번 곱할 지 


if __name__ == "__main__":
    main()
# name 은 현재 모듈의 이름 > 스크립트로 직접 실행하면 name 에는 main이 들어가고 
# 다른 모듈에서 임포트 하면 name의 값이 모듈의 이름이 됨 (파일 이름)
# 이게 가장 먼저 실행됨 > 이 스크립트에서 실행되는 것이 맞으니 > main 함수가 동작 

# 이건가 lib에 있는 martix 로 연산을 하는 거고 우리가 한 거는 인풋을 받아 문자열 > int로 바꿔준건가 
