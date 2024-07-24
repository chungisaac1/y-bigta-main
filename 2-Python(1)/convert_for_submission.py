import os

# 실제 디렉토리 경로로 수정 
# ./ 은 제일 위에 있다는 가정하에 접근 
PATH_1 = "./2-Python(1)-assignment/1-divide-and-conquer-multiplication"
PATH_2 = "./2-Python(1)-assignment/2-trie"
PATH_3 = "./2-Python(1)-assignment/3-segment-tree"

ROOT_PATH = {
    "10830": PATH_1,
    "3080": PATH_2,
    "5670": PATH_2,
    "2243": PATH_3,
    "3653": PATH_3,
    "17408": PATH_3
}
# 저장한 파일 지정 
PATH_SUB = "./2-Python(1)-assignment/submission"

def f(n: str) -> None:
    num_path = f"{ROOT_PATH[n]}/{n}.py"
    lib_path = f"{ROOT_PATH[n]}/lib.py"
    
    print(f"Processing file: {num_path}")
    print(f"Library file: {lib_path}")
    
    try:
        num_code = "".join(filter(lambda x: "from lib import" not in x, open(num_path).readlines()))
        lib_code = open(lib_path).read()
        code = lib_code + "\n\n\n" + num_code
        if not os.path.exists(PATH_SUB):
            os.makedirs(PATH_SUB)
        open(f"{PATH_SUB}/{n}.py", 'w').write(code)
    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    for k in ROOT_PATH:
        f(k)