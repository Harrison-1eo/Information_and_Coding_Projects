from ..HammingCheck import hamming_check
import sys

def main():
    hamming = hamming_check(15,11)
    
    while True:
        # 从标准输入中读入11个字符的数据
        data = sys.stdin.read(11)
        if data is None:
            break
        try:
            encoded = hamming.encode(data)
        except ValueError:
            return
        
        sys.stdout.write(encoded)
    
if __name__ == '__main__':
    main()
    
    