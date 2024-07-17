import argparse
import logging

# argparse 모듈을 사용하면 스크립트 실행 시 명령줄에서 사용할 수 있는 옵션이나 인자 설정 가능 
# -- 로 시작함 
# 파싱 > 스크립트 뒤에 명령줄을 프로그램이 알아들을 수 있게 설정하는거 
def create_parser() -> argparse.ArgumentParser: # argparse.argument > 클래스임 
    parser = argparse.ArgumentParser(description="파싱 생성") # 객체 생성 , description 파서 객체에 대한 설명 제공 > 사용자가 --help로 접근 가능 
    parser.add_argument('--start', type=int, required=True, help='The start value') # int 로 받고 , 필수 , --help 해서 볼 수있음 
    parser.add_argument('--end', type=int, required=True, help='The end value')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode') # bool 값을 갖는다 
    return parser



if __name__ == "__main__":
    parser = create_parser() # 객체 생성 및 인자 정의
    args = parser.parse_args() # 명령줄 인자 파싱 , parse_args() > argpasrse.argu 클래스 안에 내장함수 
    # 생성된 객체 parser 안에 start,end,verbose 에 접근할 수 있음 
    # 변수에 세가지 값이 들어가는 건데 > 이게 namespace 떄문에 가능한거래 
    # args 변수에는 argparse.namespace 객체가 저장된다 >
    start: int = args.start # 파싱도니 인자를 변수에 할당 
    end: int = args.end
    verbose: bool = args.verbose

    print(start, end, verbose) # 파싱된 인자 출력 

# namespace > 객체는 파이썬의 내장 클래스 중 하나로 인자의 이름과 값을 저장하는데 사용 