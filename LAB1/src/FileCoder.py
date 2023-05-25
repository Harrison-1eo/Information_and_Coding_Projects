"""
 @description: 各个窗口逻辑
 @author: Harrison-1eo
 @date: 2023-04-26
 @version: 1.0
"""

import tkinter as tk
import os
from tkinter import filedialog
import tkinter.font as font
import hashlib
import shutil
import tempfile

from FileUtil import *

# 编码模式字典
encrypt_mode_dict = {
    'Huffman编码'       : file_encode_huffman,
    'LZ78编码'          : file_encode_lz78,
    'LZ78 + Huffman编码': file_encode_lz78_huffman
}


class App:
    def __init__(self):
        self.root = tk.Tk()

    # 编码文件
    def encode_file(self, input_file_path, output_file_dir, encrypt_mode):
        if not os.path.isfile(input_file_path):
            return 0, "错误：输入文件路径必须是文件！", None
        if not os.path.exists(input_file_path):
            return 0, "错误：输入文件不存在！", None
        if not os.access(input_file_path, os.R_OK):
            return 0, "错误：输入文件不可读！", None
        if os.path.isfile(output_file_dir):
            return 0, "错误：输出文件路径必须是文件夹！", None
        if not os.path.exists(output_file_dir):
            os.makedirs(output_file_dir)
        if not os.access(output_file_dir, os.W_OK):
            return 0, "错误：输出文件夹不可写！", None

        # 获取文件名
        input_file_name = os.path.basename(input_file_path)

        # 获取输入文件名和扩展名
        input_file_name_only, input_file_ext = os.path.splitext(os.path.basename(input_file_path))

        # 编码前文件大小：
        input_file_size = os.path.getsize(input_file_path)

        # 构造输出文件路径
        output_file_name = input_file_name_only + '.enc'
        output_file_path = os.path.join(output_file_dir, output_file_name)

        with open(input_file_path, 'rb') as f:
            data = f.read()

        if data == b'':
            return 0, "错误：输入文件为空！", None
        else:
            try:
                info, res = encrypt_mode_dict[encrypt_mode](data)
            except:
                return 0, "编码发生未知错误！", None
                
                
            
        with open(output_file_path, 'wb') as f:
            f.write(input_file_name.encode('utf-8'))
            f.write(b'\n')
            f.write(info)
            f.write(b'\n')
            f.write(res)

        
        # 编码后文件大小：
        output_file_size = os.path.getsize(output_file_path)
        # 编码率：
        encode_rate = str(output_file_size / input_file_size * 100 ) + ' %'
        # 返回编码信息
        file_info = [input_file_size, output_file_size, encode_rate]
        
        return 1, output_file_path, file_info

    # 解码文件
    def decode_file(self, input_file_path, output_file_dir):
        if not os.path.isfile(input_file_path):
            return 0, "错误：输入文件路径必须是文件！"
        if not os.path.exists(input_file_path):
            return 0, "错误：输入文件不存在！"
        if not os.access(input_file_path, os.R_OK):
            return 0, "错误：输入文件不可读！"
        if os.path.isfile(output_file_dir):
            return 0, "错误：输出文件路径必须是文件夹！"
        if not os.path.exists(output_file_dir):
            os.makedirs(output_file_dir)
        if not os.access(output_file_dir, os.W_OK):
            return 0, "错误：输出文件夹不可写！"
        
        with open(input_file_path, 'rb') as f:
            try:
                name = f.readline().decode('utf-8').strip()
                info = f.readline().decode('utf-8').strip()
                data = f.read()
            except:
                return 0, "错误：文件格式错误！不是由本程序编码的文件！"

        output_file_path = os.path.join(output_file_dir, name)
        
        try:
            if info.find('lz') != -1:
                num = int(info[2:])
                res = file_decode_lz78(num, data)
            elif info.find('hu') != -1:
                num = int(info[2:])
                res = file_decode_huffman(num, data)
            elif info.find('lh') != -1:
                tmp = info.split('lh')
                num1 = int(tmp[0])
                num2 = int(tmp[1])
                res = file_decode_huffman_lz78(num2, num1, data)
            else:
                return 0, "错误：文件格式错误！不是由本程序编码的文件！"
        except:
            return 0, "解码发生未知错误！"
        
        with open(output_file_path, 'wb') as f:
            f.write(res)

        return 1, output_file_path

    # 编码正确性验证
    def check_file(self, input_file_path, encrypt_mode):
        
        # 计算原文件的哈希值
        with open(input_file_path, 'rb') as f:
            sha1 = hashlib.sha256()
            data = f.read()
            sha1.update(data)
        original_hash = sha1.hexdigest()

        # 在 input_file_path 所在目录下创建一个临时文件夹 __temp__
        temp_dir = tempfile.mkdtemp(dir = os.path.dirname(input_file_path))
        print('tmp_dir: ', temp_dir)

        try:
            # 将 input_file_path 复制到 __temp__ 中
            # encode_file = temp_dir/test.txt 源文件
            encode_file = os.path.join(temp_dir, os.path.basename(input_file_path))
            shutil.copy2(input_file_path, encode_file)

            # decode_dir = temp_dir/decoded
            decoded_dir  = os.path.join(temp_dir, 'decoded')
            # encoded_file = temp_dir/decoded/test.enc
            encoded_file = os.path.join(decoded_dir, os.path.splitext(os.path.basename(input_file_path))[0] + '.enc')
            # decoded_file = temp_dir/decoded/test.txt 加密后恢复的文件
            decoded_file = os.path.join(decoded_dir, os.path.basename(input_file_path))

            
            self.encode_file(encode_file, decoded_dir, encrypt_mode)

            self.decode_file(encoded_file, decoded_dir)

            # 计算解码后的文件的哈希值
            with open(decoded_file, 'rb') as f:
                sha2 = hashlib.sha256()
                data = f.read()
                sha2.update(data)
            decoded_hash = sha2.hexdigest()

        finally:
            # 删除 __temp__ 文件夹
            shutil.rmtree(temp_dir)
            return original_hash, decoded_hash
            

    # 编码窗口
    def encode_window(self):
        # 关闭编码窗口时的回调函数
        def on_closing():
            self.root.deiconify()            # 显示主窗口
            encode_window.destroy()     # 关闭编码文件窗口

        # 创建编码窗口
        encode_window = tk.Toplevel(self.root)
        encode_window.title("编码文件")

        self.root.withdraw()                 # 隐藏主窗口
        encode_window.protocol("WM_DELETE_WINDOW", on_closing)     # 指定关闭窗口时的回调函数
        encode_window.grab_set()        

        tk.Label(encode_window, text="选择要编码的文件:").pack()

        # 选择文件
        input_file_path_entry = tk.Entry(encode_window, width=80)
        input_file_path_entry.pack()
        def select_input_file():
            input_file_path = filedialog.askopenfilename()
            input_file_path_entry.delete(0, tk.END)
            input_file_path_entry.insert(0, input_file_path)

            output_file_path_entry.delete(0, tk.END)
            out, _ = os.path.split(input_file_path)
            out = os.path.join(out, 'encoded')
            output_file_path_entry.insert(0, out)
            encode_window.grab_set()

        tk.Button(encode_window, text="选择文件", command=select_input_file).pack()

        # 选择编码模式
        tk.Label(encode_window, text="选择编码模式:").pack()
        encrypt_mode_var = tk.StringVar()
        for mode in encrypt_mode_dict.keys():
            tk.Radiobutton(encode_window, text=mode, variable=encrypt_mode_var, value=mode).pack()
        encrypt_mode_var.set('Huffman编码')

        tk.Label(encode_window, text="选择输出文件路径：").pack()

        # 选择输出文件夹
        output_file_path_entry = tk.Entry(encode_window, width=80)
        output_file_path_entry.pack()
        def select_output_dir():
            output_file_path = filedialog.askdirectory()
            output_file_path_entry.delete(0, tk.END)
            output_file_path_entry.insert(0, output_file_path)
        
        tk.Button(encode_window, text="选择路径", command=select_output_dir).pack()

        # 开始编码
        def start_encode():
            input_file_path  = input_file_path_entry.get()
            output_file_path = output_file_path_entry.get()
            encrypt_mode     = encrypt_mode_var.get()
            res, info, file_info = self.encode_file(input_file_path, output_file_path, encrypt_mode)
            if res == 0:
                tk.messagebox.showerror("错误", info)
            else:
                size = '编码前文件大小:' + str(file_info[0]) + '字节\n编码后文件大小:' + str(file_info[1]) + '字节\n压缩率:' + file_info[2]
                tk.messagebox.showinfo("成功", "编码成功！\n编码文件为：\n" + info + "\n" + size + "\n")
                on_closing()
        
        # 开始编码按钮
        tk.Button(encode_window, text="开始编码", command=start_encode).pack()
        
    # 解码窗口
    def decode_window(self):
        # 关闭编码窗口时的回调函数
        def on_closing():
            self.root.deiconify()            # 显示主窗口
            decode_window.destroy()     # 关闭编码文件窗口

        decode_window = tk.Toplevel(self.root)
        decode_window.title("解码文件")

        self.root.withdraw()                 # 隐藏主窗口
        decode_window.protocol("WM_DELETE_WINDOW", on_closing)     # 指定关闭窗口时的回调函数
        decode_window.grab_set()

        tk.Label(decode_window, text="选择要解码的文件:").pack()
        tk.Label(decode_window, text="请选择通过本程序编码的文件").pack()

        input_file_path_entry = tk.Entry(decode_window, width=80)
        input_file_path_entry.pack()
        def select_input_file():
            input_file_path = filedialog.askopenfilename()
            input_file_path_entry.delete(0, tk.END)
            input_file_path_entry.insert(0, input_file_path)

            output_file_path_entry.delete(0, tk.END)
            out, _ = os.path.split(input_file_path)
            output_file_path_entry.insert(0, out)
            decode_window.grab_set()
        
        tk.Button(decode_window, text="选择文件", command=select_input_file).pack()

        tk.Label(decode_window, text="选择输出文件路径：").pack()

        # 选择输出文件夹
        output_file_path_entry = tk.Entry(decode_window, width=80)
        output_file_path_entry.pack()
        def select_output_dir():
            output_file_path = filedialog.askdirectory()
            output_file_path_entry.delete(0, tk.END)
            output_file_path_entry.insert(0, output_file_path)
        
        tk.Button(decode_window, text="选择路径", command=select_output_dir).pack()

        def start_decode():
            res, info = self.decode_file(input_file_path_entry.get(), output_file_path_entry.get())
            if res == 0:
                tk.messagebox.showerror("错误", info)
            else:
                tk.messagebox.showinfo("成功", "解码成功！\n解码文件为：\n" + info)
                on_closing()

        tk.Button(decode_window, text="开始解码", command=start_decode).pack()

    # 编码正确性验证窗口
    def check_window(self):
        """
        选择某一编码方式，先编码再解码，对比解码后的文件与原文件是否相同，验证哈希值是否相同
        """
        # 关闭窗口时的回调函数
        def on_closing():
            self.root.deiconify()            # 显示主窗口
            check_window.destroy()     # 关闭编码文件窗口

        # 创建验证窗口
        check_window = tk.Toplevel(self.root)
        check_window.title("编码正确性验证")
        check_window.grab_set()

        self.root.withdraw()                                             # 隐藏主窗口
        check_window.protocol("WM_DELETE_WINDOW", on_closing)       # 指定关闭窗口时的回调函数

        tk.Label(check_window, text="选择要编码的文件:").pack()

        # 选择文件
        input_file_path_entry = tk.Entry(check_window, width=80)
        input_file_path_entry.pack()
        def select_input_file():
            input_file_path = filedialog.askopenfilename()
            input_file_path_entry.delete(0, tk.END)
            input_file_path_entry.insert(0, input_file_path)

            check_window.grab_set()

        tk.Button(check_window, text="选择文件", command=select_input_file).pack()

        # 选择编码模式
        tk.Label(check_window, text="选择编码模式:").pack()
        encrypt_mode_var = tk.StringVar()
        for mode in encrypt_mode_dict.keys():
            tk.Radiobutton(check_window, text=mode, variable=encrypt_mode_var, value=mode).pack()
        encrypt_mode_var.set('Huffman编码')

        def check():
            input_file_path = input_file_path_entry.get()
            original_hash, decoded_hash = self.check_file(input_file_path, encrypt_mode_var.get())
            if original_hash == decoded_hash:
                tk.messagebox.showinfo("成功，", "编码正确！" + "\n编码前哈希值：" + original_hash + "\n编码后哈希值：" + decoded_hash)
            else:
                tk.messagebox.showerror("错误", "编码错误！\n编码前哈希值：" + original_hash + "\n编码后哈希值：" + decoded_hash)
            on_closing()

        # 开始编码按钮
        tk.Button(check_window, text="开始验证", command=check).pack()

    # 关于窗口
    def about_window(self):
        def on_closing():
            self.root.deiconify()            
            about_window.destroy()    
        
        about_window = tk.Toplevel(self.root)
        about_window.title("关于")
        about_window.grab_set()

        self.root.withdraw()                 
        about_window.protocol("WM_DELETE_WINDOW", on_closing)    

        text = tk.Text(about_window, height=6, width=30, bd=0, highlightthickness=0)
        msg = "信息论与编码第一次大作业\n姓名：Harrison-1eo\n敬请批评指正！"
        text.insert('1.0', msg)
        text.configure(state='disabled')  # 禁止编辑
        text.pack()

    # 创建主窗口
    def run(self):
        # 创建主窗口
        self.root.title("编码解码程序")
        
        # 设置主窗口字体和大小
        self.root.geometry("300x400")
        font_style = font.Font(family="Helvetica", size=12)
        self.root.option_add("*Font", font_style)
        self.root.grab_set()       
        self.root.configure(bg="#F5F5F5")

        # 创建编码按钮
        encrypt_button = tk.Button(self.root, text="编码", command=self.encode_window, width=15, height=3, bg="#5cb85c", fg="#FFFFFF", activebackground="#4cae4c", activeforeground="#FFFFFF")
        encrypt_button.pack(pady=10)

        # 创建解码按钮
        decrypt_button = tk.Button(self.root, text="解码", command=self.decode_window, width=15, height=3, bg="#d9534f", fg="#FFFFFF", activebackground="#c9302c", activeforeground="#FFFFFF")
        decrypt_button.pack(pady=10)

        # 创建编码正确性验证按钮
        check_button = tk.Button(self.root, text="编码正确性验证", command=self.check_window, width=15, height=3, bg="#f0ad4e", fg="#FFFFFF", activebackground="#ec971f", activeforeground="#FFFFFF")
        check_button.pack(pady=10)

        # 创建关于按钮
        about_button = tk.Button(self.root, text="关于", command=self.about_window, width=15, height=3, bg="#5bc0de", fg="#FFFFFF", activebackground="#46b8da", activeforeground="#FFFFFF")
        about_button.pack(pady=10)

        # 进入消息循环
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()