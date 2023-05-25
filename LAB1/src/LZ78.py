"""
 @description: LZ78编码
 @author: Harrison-1eo
 @reference : https://www.cnblogs.com/en-heng/p/6283282.html
 @date: 2023-04-21
 @version: 1.0
"""
from math import log

class LZ78:
    def __init__(self):
        pass

    @ classmethod
    def encode(cls, message: bytes):
        """
        @description: LZ78压缩算法
        @param {bytes} message: 待压缩的字符串
        @return: 返回一个生成器，每次迭代返回一个元组，元组中第一个元素为距离，第二个为结束字符
                 用 list() 函数将其转换为列表
                 注意列表最后一个元素为 ('end', 索引的编码长度)
        """
        # 定义一个空的字典 tree_dict，用于存储字符串中出现过的子串
        # 定义 m_len 为字符串 message 的长度，i 初始值为 0
        tree_dict = {}
        m_len     = len(message)
        i         = 0
        
        while i < m_len:
            # Case I: 如果当前字符不在字典 tree_dict 中，则输出 (0, 当前字符)，
            # 并将当前字符加入字典 tree_dict 中，键值为当前字符的 ASCII 码值加 1
            if message[i:i+1] not in tree_dict.keys():
                yield (0, message[i:i+1])
                tree_dict[message[i:i+1]] = len(tree_dict) + 1
                i += 1
            
            # Case III: 如果已经到了字符串的末尾，则输出 (当前子串的键值, '')，
            # 并结束循环
            elif i == m_len - 1:
                yield (tree_dict.get(message[i:i+1]), b'')
                i += 1
                
            
            # Case II: 如果当前字符在字典 tree_dict 中，需要寻找以当前字符为开头的最长子串，
            # 使得这个子串不在字典 tree_dict 中
            else:
                for j in range(i + 1, m_len):
                    # 如果从当前位置到 j 位置的子串不在字典 tree_dict 中，
                    # 则输出 (当前子串的键值, j 位置上的字符)，并将这个子串加入字典 tree_dict 中
                    if message[i:j + 1] not in tree_dict.keys():
                        yield (tree_dict.get(message[i:j]), message[j:j+1])
                        tree_dict[message[i:j + 1]] = len(tree_dict) + 1
                        i = j + 1
                        break
                    
                    # 如果已经到了字符串的末尾，则输出 (当前子串的键值, '')，
                    # 并结束循环
                    elif j == m_len - 1:
                        yield (tree_dict.get(message[i:j + 1]), b'')
                        i = j + 1
                        
            if i == m_len:
                yield ('end', int(log(len(tree_dict), 256)) + 1)

    @ classmethod
    def list_to_bytes(cls, msg: list) -> tuple[int, bytes]:
        res = b''
        length = msg[-1][1]
        msg = msg[:-1]
        for index, alpha in msg:
            # 元组的第一位是索引，第二位是字符
            # 将索引都填充到length字节，字符不填充
            res += index.to_bytes(length=length, byteorder='big').zfill(length)
            if alpha != b'' and alpha is not None:
                res += alpha

        return length, res

    @ classmethod
    def decode(cls, packed) -> bytes:
        """
        @description: LZ78解压缩算法
        @param {list} packed: 待解压缩的列表，注意最后没有end标志
        @return: 返回解压缩后的字节串
        """
        # file = open('lz78_log.txt', 'w')

        unpacked, tree_dict = b'', {}
        
        # 遍历压缩后的字符串中的每个键值对
        for index, ch in packed:
            # index: int, ch: bytes

            # if ch != '': 
            #     file.write('index: ' + str(index) + ' ch: ' + str (int.from_bytes(ch, byteorder='big')) + '\n')
            # else:
            #     file.write('index: ' + str(index) + ' ch: ' + '\'\'' + '\n')
            
            # 如果键值 `index` 为 0，则说明 `ch` 是一个新的字符
            if index == 0:
                # 将 `ch` 添加到解压缩后的字符串 `unpacked` 中，并将其加入字典 `tree_dict` 中，
                # 键值为字典中元素的个数加 1
                unpacked += ch
                tree_dict[len(tree_dict) + 1] = ch
            # 否则，`ch` 是一个子串的结尾字符
            else:
                # 根据字典 `tree_dict` 中对应的键值 `index` 来构建完整的子串 `term`，
                # 将 `term` 添加到解压缩后的字符串 `unpacked` 中，并将其加入字典 `tree_dict` 中，
                # 键值为字典中元素的个数加 1
                term = tree_dict.get(index) + ch
                unpacked += term
                tree_dict[len(tree_dict) + 1] = term

                # file.write('term: ' + str(term) + '\n')
        
        # 返回解压缩后的字符串
        return unpacked


if __name__ == '__main__':
    messages = [b'ABBCBCABABCAABCABCAACBACCABCCABCAACCCCACAAB', b'BABAABRRRA', b'AAAAAAAAA']
    for m in messages:
        print(m)
        # 返回值为一个生成器，需要使用 list() 函数将其转换为列表
        pack = LZ78.encode(m)
        pack = list(pack)
        print(pack)
        unpack = LZ78.decode(pack[:-1])
        print(unpack)
        print(unpack == m)
