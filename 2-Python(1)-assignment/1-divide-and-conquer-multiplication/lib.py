from __future__ import annotations
import copy


"""
TODO:
- __setitem__ 구현하기 
- __pow__ 구현하기 (__matmul__을 활용해봅시다)
- __repr__ 구현하기
"""


class Matrix:
    MOD = 1000

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    @staticmethod # 지정된 값으로 채워진 행렬을 생성 
    def full(n: int, shape: tuple[int, int]) -> Matrix:
        return Matrix([[n] * shape[1] for _ in range(shape[0])])

    @staticmethod # 모든 요소가 0인 행렬 생성 
    def zeros(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(0, shape)

    @staticmethod # 모든 요소가 1인 행렬 생성 
    def ones(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(1, shape)

    @staticmethod # 단위 행렬을 생성 
    def eye(n: int) -> Matrix:
        matrix = Matrix.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1
        return matrix

    @property # 클래스의 메소드를 속성처럼 사용할 수 있게 > 이렇게 하면 shpae를 속성처럼 접근이 가능 함수가 아니라 > 편리하게 사용가능 
    def shape(self) -> tuple[int, int]:
        return (len(self.matrix), len(self.matrix[0]))

    def clone(self) -> Matrix: # 복사본 만들기 
        return Matrix(copy.deepcopy(self.matrix))

    def __getitem__(self, key: tuple[int, int]) -> int: # 객체의 특정 항목을 가져올 때 
        return self.matrix[key[0]][key[1]] # key를 통해서 찾는다 0번째 값으로 행 선택 1로 열 선택 

    def __setitem__(self, key: tuple[int, int], value: int) -> None: # 객체의 특정 항목을 설정하는 동작을 재정의
        # self.matrix[key[0]][key[1]] = value
        self.matrix[key[0]][key[1]] = value % self.MOD
        # matrix[1,1]= 1001 > 1001이 value 
        # self.MOD > matrix 클래스의 정적 변수로 행렬의 모든 요소를 특정 숫자로 나눈 나머지로 저장하도록 강제하는 역할 
        # 여기서는 1000으로 함 > 0~999 사이의 값을 가지도록  > 큰 수를 다루기 쉽게, 효율성 



        # 구현하세요!
        pass

    def __matmul__(self, matrix: Matrix) -> Matrix: # @ 연산자를 사용하여 행렬 곱셈을 수행하는 메서드 
        x, m = self.shape # property 해서 이렇게 쓸 수 있는 듯 
        m1, y = matrix.shape # shpae 위에 있음  
        assert m == m1 # m과 m1 맞아야 실행됨 
        # 조건이 참이 아니면 assertionError를 발생시킴 

        result = self.zeros((x, y))
        # 새로 담을 그릇 만들기 > x행 , y열 개수로 크기 가 나오니까  

        for i in range(x):
            for j in range(y):
                for k in range(m):
                    result[i, j] += self[i, k] * matrix[k, j]
        # 돌아가면서 계산 

        return result
    # A = Matrix([[1, 2], [3, 4]]) C = A @ B
    # print(C)  # 출력: [[4, 4], [10, 8]]

    def __pow__(self, n: int) -> Matrix: # ** 연사자를 사용하여 행렬의 거듭제곱을 수행하는 메소드 
        result = self
        for _ in range(n-1):
            result = result @ self 
             
        return result 
        # self.matrix 가 아니라 self 인 이유 > self.matrix 는 데이터 값만 담고 있는 거임 연산을 수행하지 못 함 객체에 접근해야 연산 가능 
    def __pow__(self, n: int) -> 'Matrix':
        # 거듭제곱 분할법을 사용함 n만큼 생성해서 거듭제곱 
        result = Matrix.eye(len(self.matrix)) # 단위행렬 생성 > n * n 크기의 단위행렬 생성
        base = self

        while n > 0:
            if n % 2 == 1: # 나머지 
                result = result @ base
            base = base @ base
            n //= 2 # 몫 
        return result
    
    def __repr__(self) -> str: # 객체의 문자열 표현을 반환하는 메소드 
         # 행렬의 각 행을 문자열로 변환하고, 줄 바꿈 문자를 사용하여 행을 구분
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])
        
