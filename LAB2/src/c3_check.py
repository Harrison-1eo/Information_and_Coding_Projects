import hashlib
import random
from HammingCheck import hamming_check

hamming = hamming_check(15, 11)
# msg 中存储编码前的数据，和使用hamming_matrix编码后的数据
msg = []

with open('./lab2_data/hamming_15_11.txt', 'r') as f:
    # 读取数据
    for line in f.readlines():
        code, coded = line.strip().split(' ')
        hamming_code = hamming.encode(code[:-1])
        if hamming_code != coded:
            print(code, coded, hamming_code, 'encode error')
        else:
            msg.append((code[:-1], hamming_code))
    
with open('./test/hamming_c3.txt', 'wb') as f:
    for i in range(len(msg)):
        if i != len(msg) - 1:
            f.write((msg[i][0] + ', ' + msg[i][1] + '\n').encode('utf-8'))
        else:
            f.write((msg[i][0] + ', ' + msg[i][1]).encode('utf-8'))
        
    
# 计算前后文件的hash值
with open('./lab2_data/hamming_15_11.txt', 'rb') as f:
    hash1 = hashlib.md5(f.read()).hexdigest()
    print('./lab2_data/hamming_15_11.txt hash: ', hash1)
    
with open('./test/hamming_c3.txt', 'rb') as f:
    hash2 = hashlib.md5(f.read()).hexdigest()
    print('./test/hamming_c3.txt hash: ', hash2)
    
if hash1 == hash2:
    print('hash check passed')


# 计算解码后的数据，并输出    
for code, coded in msg:
    decode = hamming.decode(coded)
    if code != decode:
        print('decode error')
        break
    else:
        print(coded, '->', decode, 'decode success'.upper())
        

# 随机选取一个位置，将该位置的值取反，再进行解码
for code, coded in msg:
    # 随机选取一个位置，将该位置的值取反
    pos = random.randint(0, len(coded) - 1)
    coded = coded[:pos] + str(int(coded[pos]) ^ 1) + coded[pos + 1:]
    decode = hamming.decode(coded)
    if code != decode:
        print('decode error')
        break 
    else:
        print("change pos %2d" % pos , coded, '->', decode, 'decode success'.upper())
    
