"""
 @description: Huffman编码
 @author: Harrison-1eo
 @date: 2023-04-22
 @version: 1.0
"""

import sys
# 修改最大递归深度
sys.setrecursionlimit(1000000)	  

class node(object):
    """
    @description: 哈夫曼树结点的类定义
    """
    def __init__(self, value = None, left = None, right = None, father = None):
        """
        @description: 初始化结点
        @param {int} value - 结点的权重
        @param {node} left - 左结点
        @param {node} right - 右结点
        @param {node} father - 父结点
        """
        self.value = value
        self.left = left
        self.right = right
        self.father = father

class Huffman(object):

    def __init__(self):
        pass

    @ classmethod
    def find_insert_pos(cls, l: list[node], num):
        # 找到l中第一个大于num的位置
        for i in range(len(l)):
            if l[i].value > num:
                return i
        return len(l)

    @ classmethod
    def creat_tree(cls, nodes_list: list[node]) -> node:
        """
        @description: 构建哈夫曼树，递归实现
        @param {list} nodes_list - 结点列表
        @return {node} - 根结点
        """
        # 将结点列表进行升序排序
        nodes_list.sort(key = lambda x: x.value)      
        
        # 只有一个结点时，返回根结点
        if len(nodes_list) == 1:
            return nodes_list[0]        
        
        # 创建最小的两个权重结点的父节点
        father_node = node(nodes_list[0].value + nodes_list[1].value, nodes_list[0], nodes_list[1]) #创建最小的两个权重结点的父节点
        nodes_list[0].father = nodes_list[1].father = father_node
        
        # 删除最小的两个结点并加入父结点
        nodes_list.pop(0)
        nodes_list.pop(0)
        nodes_list.insert(cls.find_insert_pos(nodes_list, father_node.value), father_node)

        if len(nodes_list) > 1:
            nodes_list[0], nodes_list[1] = nodes_list[1], nodes_list[0]   

        return cls.creat_tree(nodes_list)

    @ classmethod
    def node_encode(cls, node1: node) -> bytes:
        """
        @description: 对叶子结点进行编码
        @param {node} node1 - 叶子结点
        @return {bytes} - 叶子结点的编码
        """
        if node1.father == None:
            return b''
        if node1.father.left == node1:
            return cls.node_encode(node1.father) + b'0'
        else:
            return cls.node_encode(node1.father) + b'1'

    @ classmethod
    def sort_dict(cls, d: dict) -> dict:
        """
        @description: 对字典按照值进行排序，重新赋值为从 0 开始的整数，最大值为255，保证编码后的字节长度为 1
        @param {dict} d - 待排序的字典
        @return {dict} - 排序后的字典
        """
        sorted_pairs = sorted(d.items(), key=lambda x: x[1])
        new_values = [0]
        for i in range(1, len(sorted_pairs)):
            if sorted_pairs[i][1] == sorted_pairs[i-1][1]:
                new_values.append(new_values[i-1])
            else:
                new_values.append(new_values[i-1]+1)
        return {k:v for (k,_),v in zip(sorted_pairs, new_values)}     
    
    @ classmethod
    def encode(cls, msg: bytes) -> tuple[bytes, bytes]:
        """
        @description: Huffman 编码压缩
        @param {str} msg - 待压缩的内容
        @return {info} - 压缩信息
        @return {bytes} - 压缩后的文件
        """
        # bytes_list = msg.encode(encoding = 'UTF-8')
        bytes_list = msg
        size = len(bytes_list)

        # bytes_list 中存放的是文件内容的每个字节，即每个字节的 ASCII 码
        # size 为文件的总长度
        # count_dict 为字典，key 为字节，val 为出现的次数
        # 统计各字节出现的频率
        # print('统计各字节出现频率中...\n')
        count_dict = {}
        for x in bytes_list:
            if x not in count_dict.keys():
                count_dict[x] = 0
            count_dict[x] += 1

        count_dict = cls.sort_dict(count_dict)
        # print(count_dict)

        # 使用一个字典将count_list中的值node化,其中key为对应的字符，值为字符对应的结点
        # nodes_dict 为字典，key 为字节，val 为对应的结点，结点的权重即 count_dict[x]
        # nodes_list 为结点列表
        nodes_dict = {}   
        for x in count_dict.keys():
            nodes_dict[x] = node(count_dict[x])  
        nodes_list = [nodes_dict[x] for x in nodes_dict.keys()]
         

        # 构建哈夫曼树
        root = cls.creat_tree(nodes_list)   

        # bytes_dict 为字典，key 为字节，val 为对应的编码
        # 对叶子结点编码，输出字节与哈夫曼码的字典
        bytes_dict = {}
        for x in nodes_dict.keys():
            bytes_dict[x] = cls.node_encode(nodes_dict[x])
        if len(bytes_dict) == 1:
            bytes_dict[list(bytes_dict.keys())[0]] = b'0'


        info = b''
        encode_res = b''

        # 写入结点以及对应频率
        for x in count_dict.keys():
            # object.write(x)
            # object.write(int.to_bytes(count_dict[x], width, byteorder='big'))
            info += int.to_bytes(x            , 1, byteorder='big')
            info += int.to_bytes(count_dict[x], 1, byteorder='big')
            # print(x,':',count_dict[x], bytes_dict[x])
        
        # 写入数据，注意每次要凑一个字节
        code = ''     
        for x in bytes_list:
            code += bytes_dict[x].decode(encoding = 'UTF-8')
            out = 0
            while len(code) >= 8:
                for s in range(8):
                    out = out << 1
                    if code[s] == '1':
                        out = out | 1
                # object.write(int.to_bytes(out,1,byteorder='big'))
                encode_res += int.to_bytes(out, 1, byteorder='big')
                out = 0
                code = code[8:]

        
        # 处理可能不足一个字节的数据
        # 采用补0的方式，并在最后一节数据中写入补零的个数
        if len(code) != 0:
            left = 8 - len(code)
            for i in range(left):
                code += '0'
            for s in range(8):
                out = out << 1
                if code[s] == '1':
                    out = out | 1
            encode_res += int.to_bytes(out , 1, byteorder='big')
            encode_res += int.to_bytes(left, 1, byteorder='big')
        else:
            encode_res += int.to_bytes(0, 1, byteorder='big')

        # print('压缩完成！')

        # print(info)
        # print(encode_res)
        return info, encode_res

    @ classmethod
    def decode(cls, info: bytes, msg: bytes) -> bytes:
        """
        @description: Huffman解压缩
        @param {bytes} info: 压缩文件的头部信息，包含频率位宽、结点信息
        @param {bytes} msg : 压缩文件的01串
        @return {bytes} res: 解压缩后的文件
        """
        count_dict = {}
        i = 0
        while i < len(info):
            # 先读出字节，再读出频率
            # print(i, info[i])
            dict_key   = int.from_bytes(info[i: i + 1], byteorder='big')
            i += 1
            # print(i, info[i])
            dict_value = int.from_bytes(info[i: i + 1], byteorder='big')
            i += 1
            count_dict[dict_key] = dict_value
            

        # print('生成反向字典中...')
        #以下过程与编码时的构建过程相同
        nodes_dict = {}   
        for x in count_dict.keys():
            nodes_dict[x] = node(count_dict[x])  
        nodes_list = [nodes_dict[x] for x in nodes_dict.keys()]

        root = cls.creat_tree(nodes_list)   

        bytes_dict = {}
        for x in nodes_dict.keys():
            bytes_dict[x] = cls.node_encode(nodes_dict[x]).decode(encoding = 'UTF-8')
        # for x in bytes_dict.keys():
            # print(x,':',bytes_dict[x])

        # print(bytes_dict)
        # 生成反向字典, key为编码, value为对应的字节
        diff_dict = {}
        for x in bytes_dict.keys():
            diff_dict[bytes_dict[x]] = x


        # print('解码中...')
        # msg = ''.join([format(x, '08b') for x in msg]).lstrip('0')
        tmp = ''
        for i in msg:
            tmp += bin(i)[2:].zfill(8)
        msg = tmp
        # print(msg)
        
        # print(msg)

        # 处理填充
        left = int(msg[-8:], 2)
        msg = msg[:-8-left]
        # print(msg)

        size = len(msg)

        decode_res = b''

        # 解码时不停读取单个数字，遍历二叉树，直到找到叶子结点
        i = 0
        while i < size:
            node_now = root
            key = ''
            while node_now.left != None and node_now.right != None:
                if msg[i] == '0':
                    node_now = node_now.left
                    key += '0'
                else:
                    node_now = node_now.right
                    key += '1'
                i += 1
            # print(key, chr(diff_dict[key]))
            decode_res += diff_dict[key].to_bytes(1, byteorder='big')

        # print('解压成功！')
        return decode_res

    @ classmethod
    def decode_one_letter(cls, info: bytes, msg: bytes) -> bytes:
        value = info[0:1]

        left = msg[-1]
        length = (len(msg) - 1) * 8 - left

        res = value * length

        return res

        
if __name__ == '__main__':
    msg = b'ABBCBCABABCAABCABCAACBACCABCCABCAACCCCACAAB'
    info, enc = Huffman.encode(msg)
    print(info)
    print(enc)
    ans = Huffman.decode(info, enc)
    print(ans)
    print(ans == msg)



