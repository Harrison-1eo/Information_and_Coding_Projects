"""
 @description: 文件操作工具类，包括对文件使用huffman编码和解码，使用LZ78编码和解码，两者结合的编码和解码
 @author: Harrison-1eo
 @date: 2023-04-26
 @version: 1.0
"""

from Huffman import Huffman
from LZ78 import LZ78

def file_encode_huffman(msg: bytes) -> tuple[bytes, bytes]:
    """
    @description - 对文件使用huffman编码
    @param {bytes} msg - 文件内容
    @return {tuple[bytes, bytes]} - (文件类型, 编码结果)
    """
    print(" ======== file_encode_huffman ======== ")

    info, encode_res = Huffman.encode(msg)
    info_len = len(info)

    type = ('hu' + str(info_len)).encode(encoding='UTF-8')
    res = info + encode_res
    
    return type, res

def file_decode_huffman(info_len: int, msg: bytes) -> bytes:
    """
    @description: 对文件使用huffman解码
    @param {int} info_len - 文件类型信息长度
    @param {bytes} msg - 文件内容
    @return {bytes} - 解码结果
    """
    print(" ======== file_decode_huffman ======== ")
    
    info = msg[:info_len]
    msg  = msg[info_len:]
    if info_len == 2:
        res = Huffman.decode_one_letter(info, msg)
    else:
        res = Huffman.decode(info, msg)

    return res

def file_encode_lz78(msg: bytes) -> tuple[bytes, bytes]:
    """
    @description: 对文件使用LZ78编码
    @param {bytes} msg - 文件内容
    @return {tuple[bytes, bytes]} - (文件类型, 编码结果)
    """
    print(" ======== file_encode_lz78 ======== ")

    res = LZ78.encode(msg)
    res = list(res)

    length, msg = LZ78.list_to_bytes(res)

    type = ('lz' + str(length)).encode(encoding='UTF-8')
    res  = msg
    return type, res

def file_decode_lz78(length: int, msg: bytes) -> bytes:
    """
    @description: 对文件使用LZ78解码
    @param {int} length - 文件类型信息长度
    @param {bytes} msg - 文件内容
    @return {bytes} - 解码结果
    """
    print(" ======== file_decode_lz78 ======== ")
    
    flag = False
    if len(msg) % (length + 1) != 0:
        flag = True

    content = []
    for i in range(0, len(msg) - length - 1, length + 1):
        content.append((int.from_bytes(msg[i:i+int(length)], byteorder='big'), msg[i+int(length):i+int(length)+1]))
    
    if flag:
        content.append((int.from_bytes(msg[-length:], byteorder='big'), b''))
    else:
        content.append((int.from_bytes(msg[-length-1:-1], byteorder='big'), msg[-1:]))

    res = LZ78.decode(content)

    return res

def file_encode_lz78_huffman(msg: bytes) -> tuple[bytes, bytes]:
    """
    @description: 对文件先使使用LZ78编码，再使用huffman编码
    @param {bytes} msg - 文件内容
    @return {tuple[bytes, bytes]} - (文件类型, 编码结果)
    """

    print(" ======== file_encode_lz78_huffman ======== ")

    res = LZ78.encode(msg)
    res = list(res)
    
    length, msg = LZ78.list_to_bytes(res)

    info, encode_res = Huffman.encode(msg)
    info_len = len(info)

    type = str(length) + 'lh' + str(info_len)
    type = type.encode(encoding='UTF-8')
    res = info + encode_res
    return type, res

def file_decode_huffman_lz78(info_len: int, length: int, msg: bytes) -> bytes:
    """
    @description: 对文件先使使用huffman解码，再使用LZ78解码
    @param {int} info_len - 文件类型信息长度
    @param {int} length - 文件类型信息长度
    @param {bytes} msg - 文件内容
    @return {bytes} - 解码结果
    """
    print(" ======== file_decode_huffman_lz78 ======== ")

    info = msg[:info_len]
    msg  = msg[info_len:]

    msg = Huffman.decode(info, msg)

    flag = False
    if len(msg) % (length + 1) != 0:
        flag = True

    content = []
    for i in range(0, len(msg) - length - 1, length + 1):
        content.append((int.from_bytes(msg[i:i+int(length)], byteorder='big'), msg[i+int(length):i+int(length)+1]))
    
    if flag:
        content.append((int.from_bytes(msg[-length:], byteorder='big'), b''))
    else:
        content.append((int.from_bytes(msg[-length-1:-1], byteorder='big'), msg[-1:]))
    
    res = LZ78.decode(content)

    return res

if __name__ == '__main__':
    # file = '.\\testfiles\\testfile'
    # # file_encode_huffman(file, '.hf')
    # # file_encode_lz78(file, '.lz')
    # file_encode_lz78_huffman(file, '.hflz')
    file = '.\\testfiles\\testfile.hflz'
    file_decode_huffman_lz78(file)

    # file = '.\\testfiles\\testfile.lz'
    # file_decode_lz78(file)

    # print(" ======== test ======== ")
    # print(encode == decode)

    # a = str(encode)
    # with open('log_encode', 'w') as f:
    #     f.write(a)
    # b = str(decode)
    # with open('log_decode', 'w') as f:
    #     f.write(b)
    # print(a == b) 

