"""
 @project: c1.py
 @description: (15, 11)汉明码，使用生成矩阵和校验矩阵
 @author: Harrison-1eo
 @date: 2023-05-10
 @version: 1.0
"""
def print_matrix(matrix):
    """
    矩阵打印函数
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j], end=' & ')
        print('\\\\')
    print()


def multi_matrix(A, B):
    """
    矩阵乘法，A为m*n矩阵，B为n*p矩阵，返回m*p矩阵
    """
    if len(A[0]) != len(B):
        print(len(A[0]), len(B))
        raise ValueError("矩阵A的列数与矩阵B的行数不相等")
        
    C = [[0 for i in range(len(B[0]))] for j in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]

    return C


class hamming_matrix:
    def __init__(self, N, K, log=False):
        self.N = N
        self.K = K
        self.R = N - K
        self.H, tmp, ch = self.gen_H_matrix()
        self.G          = self.gen_G_matrix(tmp, ch[::-1])
        
        # 将H和G矩阵中元素转换为int
        for i in range(self.R):
            for j in range(self.N):
                self.H[i][j] = int(self.H[i][j])
        for i in range(self.K):
            for j in range(self.N):
                self.G[i][j] = int(self.G[i][j]) 
                
        if log:
            print("H:")
            print_matrix(self.H)
                
            print("G:")
            print_matrix(self.G)
                  
    def gen_H_matrix(self):
        """
        生成H校验矩阵
        """
        N, K, R = self.N, self.K, self.R
        
        # 将H矩阵的每一列转换为二进制数，从1到2**R-1
        H = [[0 for i in range(N)] for j in range(R)]
        res = [[0 for i in range(N)] for j in range(R)]
        for i in range(1, 2 ** R):
            num = bin(i)[2:].zfill(R)
            num = list(num)[::-1]
            for j in range(R):
                H[j][i - 1] = num[j]
                res[j][i - 1] = num[j]
        # res和H中存储的是 0 - 2**R-1 的二进制数
        
        # 将H的后R列变为单位矩阵
        # ch用于记录H的列交换情况
        count = 0
        ch = []
        while count < R:
            for i in range(N):
                num = [H[j][i] for j in range(R)][::-1]
                if num.count('1') == 1:
                    ptr = N - num.index('1') - 1
                    # print(ptr, i, num)
                    for j in range(R):
                        H[j][ptr], H[j][i] = H[j][i], H[j][ptr]
                    ch.append((i, ptr))
                    count += 1
                    break
                
        # 将H的前K列按照字典序排序
        for i in range(K):
            for j in range(i + 1, K):
                Hi = "".join(H[k][i] for k in range(R))[::-1]
                Hj = "".join(H[k][j] for k in range(R))[::-1]
                if Hi > Hj:
                    for k in range(R):
                        H[k][i], H[k][j] = H[k][j], H[k][i]
                    ch.append((i, j))
                    
                    
        return res, H, ch
    
    def gen_G_matrix(self, H: list, ch: list):
        N, K, R = self.N, self.K, self.R
        
        # 生成G矩阵, 前K列为单位矩阵，后R列为H的转置
        G = [[0 for i in range(N)] for j in range(K)]
        for i in range(K):
            G[i][i] = 1
        for i in range(R):
            for j in range(K):
                G[j][i + K] = H[i][j]
        
        # 输出当前的G矩阵
        # print("G_tmp:")
        # print_matrix(G)
        
        # 根据ch，交换G的列，做相同的变换
        for i, j in ch:
            for k in range(K):
                G[k][i], G[k][j] = G[k][j], G[k][i]
        return G
    
    def encode(self, msg: str) -> str:
        N, K, R = self.N, self.K, self.R
        if len(msg) != K:
            raise ValueError('msg length error')
        msg  = [[int(i) for i in msg]]
        
        code = multi_matrix(msg, self.G)[0]
        
        return ''.join(str(i & 1) for i in code)

    def decode(self, msg: str) -> str:
        N, K, R = self.N, self.K, self.R
        if len(msg) != N:
            raise ValueError('msg length error')
        msg_matrix = [[int(i)] for i in msg]
        
        check = multi_matrix(self.H, msg_matrix)
        
        wrong = ''
        for i in range(R):
            wrong += str(check[i][0] & 1)
        wrong = int(wrong[::-1], 2)

        msg = list(msg)
        if wrong != 0:
            msg[wrong - 1] = str(int(msg[wrong - 1]) ^ 1)        
        
        # msg中2^i位存储的是校验位，剩余为信息位，将信息位提取出来
        res = ''
        for i in range(len(msg)):
            if i & (i + 1) != 0:
                res += msg[i]
                
        return res
            

if __name__ == '__main__':
    h = hamming_matrix(15, 11, True)

    # 001110010100000
    code = '001110010100000'
    for i in range(15):
        tmp = list(code)
        tmp[i] = str(int(tmp[i]) ^ 1)
        tmp = ''.join(tmp)
        decode = h.decode(tmp)
        print('decode: ', tmp)
        print('correct: ', decode == '11000100000')
    

        