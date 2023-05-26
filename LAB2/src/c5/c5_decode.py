from ..HammingCheck import hamming_check
import sys

def main():
    hamming = hamming_check(15,11)
    
    while True:
        # 从标准输入中读取11个字符的数据
        data = sys.stdin.read(15)
        if not data:  # 如果无法再读取数据，退出循环
            break
        
        try:
            decoded = hamming.decode(data)
        except ValueError:
            return
        
        sys.stdout.write(decoded)
    
if __name__ == '__main__':
    main()
    
    