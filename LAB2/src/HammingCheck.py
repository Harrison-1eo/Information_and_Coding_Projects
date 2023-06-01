"""
 @project: c3.py
 @description: (15, 11)汉明码，使用奇偶校验方法
 @author: Harrison-1eo
 @date: 2023-05-25
 @version: 1.1 添加if_enhance选项
"""

class hamming_check:
    def __init__(self, N, K, if_enhance=False):
        self.N = N
        self.K = K
        self.R = N - K
        self.if_enhance = if_enhance
        
    def encode(self, msg: str) -> str:
        if len(msg) != self.K:
            raise ValueError("msg length error")
        
        
        # 生成校验位的索引，index[i]表示第i个校验位的索引
        index = [[] for _ in range(self.R)]
        for i in range(1, self.N + 1): 
            if i & (i - 1) == 0:
                continue
            for j in range(self.R):
                if i & (1 << j):
                    index[j].append(i)
        
                    
        msg = [int(i) for i in msg]
        res = [0 for _ in range(self.N)]
        # 先将信息位放入
        for i in range(1, self.N + 1): 
            if i & (i - 1) == 0:
                continue
            res[i - 1] = msg.pop(0)
        
            
        # 计算校验位
        for i in range(self.R):
            res[2 ** i - 1] = sum([res[j - 1] for j in index[i]]) % 2
    
        return ''.join([str(i) for i in res])
    
    def decode(self, msg: str):
        if len(msg) != self.N:
            raise ValueError("msg length error")
        
        # one存放所有为1的位的索引，从1开始
        msg = [int(i) for i in msg]
        one = []
        for index, i in enumerate(msg):
            if i == 1:
                one.append(index + 1)
        
        # 将所有为1的位的索引异或，得到错误位的索引
        wrong = 0
        for i in one:
            wrong ^= i
        if wrong != 0:
            msg[wrong - 1] ^= 1
        
        # 取出信息位    
        res = ''
        for i in range(self.N):
            if i & (i + 1) != 0:
                res += str(msg[i])
                
        if self.if_enhance:
            return res, wrong    
        else:    
            return res
                
    
if __name__ == '__main__':
    h = hamming_check(15, 11)
    
    print(h.encode('00000000001'))
    # print('001110010100000')
    # print(h.decode('001110010100000'))
    
    # code = '001110010100000'
    # for i in range(15):
    #     tmp = list(code)
    #     tmp[i] = str(int(tmp[i]) ^ 1)
    #     tmp = ''.join(tmp)
    #     decode = h.decode(tmp)
    #     print('decode: ', tmp)
    #     print('correct: ', decode == '11000100000')
                
                


