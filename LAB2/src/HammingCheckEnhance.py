"""
 @project: HammingCheckEnhance.py
 @description: (15, 11)汉明码，使用奇偶校验方法，增强版，可以检测两位错误，但不能纠正两位错误
 @author: Harrison-1eo
 @date: 2023-05-29
 @version: 1.0
"""
from HammingCheck import hamming_check


class hamming_check_enhance:
    def __init__(self, N, K):
        self.N = N - 1
        self.K = K
        self.R = N - K
        self.hamming_check = hamming_check(self.N, self.K, True)
    
    def encode(self, msg: str) -> str:
        res = self.hamming_check.encode(msg)
        
        num = res.count('1') % 2
        return res + str(num)
    
    def decode(self, msg: str) -> str:
        if len(msg) != self.N + 1:
            raise ValueError("msg length error")
        
        chk = msg.count('1') % 2
        res, wrong = self.hamming_check.decode(msg[:-1])
        
        condition = ''
        
        if   wrong != 0 and chk == 0:
            return None, "two bit error"
        elif wrong != 0 and chk == 1:
            return res, "one bit error"
        elif wrong == 0 and chk == 0:
            return res, "no error"
        elif wrong == 0 and chk == 1:
            return res, "chk position error"
        else:
            return None, "unknown error"
        

if __name__ == '__main__':
    import random
    h = hamming_check_enhance(16, 11)
    
    # 11100100000, 011011010100000
    code_ori = '11100100000'
    code = h.encode(code_ori)
    print(code)
    
    # 随机引入1位错误
    for _ in range(5):
        code = h.encode(code_ori)
        index = random.randint(0, 14)
        code = list(code)
        code[index] = str(1 - int(code[index]))
        code = ''.join(code)
        print(f'one bit error: {index:5}', code, '->', h.decode(code)[1], h.decode(code)[0])
    print()    
    # 随机引入2位错误
    for _ in range(5):
        code = h.encode(code_ori)
        index = random.sample(range(15), 2)
        code = list(code)
        code[index[0]] = str(1 - int(code[index[0]]))
        code[index[1]] = str(1 - int(code[index[1]]))
        code = ''.join(code)
        print(f'two bit error: {index[0]:2} {index[1]:2}', code, '->', h.decode(code)[1])    
            
        
        
    
            
        
        
        
        
        
        
