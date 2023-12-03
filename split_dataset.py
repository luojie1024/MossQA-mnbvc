#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2023/12/3 15:58 
# @Author  : Roger 
# @Version : V 0.1
# @Email   : 550997728@qq.com
# @File    : split_dataset.py

import json
import os


def merge_jsonl(input_files, output_file):
    with open(output_file, 'w', encoding='utf-8') as output:
        for input_file in input_files:
            with open(input_file, 'r', encoding='utf-8') as f:
                output.write(f.read())


def split_jsonl(input_file, output_prefix, max_file_size):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_file_size = 0
    current_file_index = 1
    current_output_file = f"{output_prefix}_{current_file_index}.jsonl"

    with open(current_output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            line_size = len(line.encode('utf-8'))
            if current_file_size + line_size > max_file_size:
                current_file_index += 1
                current_file_size = 0
                current_output_file = f"{output_prefix}_{current_file_index}.jsonl"
                f.close()
                f = open(current_output_file, 'w', encoding='utf-8')

            f.write(line)
            current_file_size += line_size


if __name__ == '__main__':
    root = 'data/sample'
    # 输入的JSONL文件列表
    input_files = [
        os.path.join(root, 'moss-002-sft-data.json'),
        os.path.join(root, 'moss-003-sft-data.json'),
        os.path.join(root, 'moss-003-sft-data-plugin.json')
    ]

    merged_file = os.path.join(root, 'merged.jsonl')  # 合并后的JSONL文件
    output_prefix = os.path.join(root, "moss_sft")  # 输出文件的前缀
    max_file_size = 500 * 1024 * 1024  # 指定的最大文件大小，这里设置为1MB

    merge_jsonl(input_files, merged_file)
    split_jsonl(merged_file, output_prefix, max_file_size)
