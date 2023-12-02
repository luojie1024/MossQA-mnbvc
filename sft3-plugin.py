#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2023/11/18 09:52 
# @Author  : Roger 
# @Version : V 0.1
# @Email   : 550997728@qq.com
# @File    : main.py
import os.path
import re
import os
from tqdm import tqdm
import json
import hashlib
from datetime import datetime


def get_hashid(content):
    return hashlib.md5((content).encode("utf-8")).hexdigest()


class QAParser(object):
    def __init__(self, source, model):
        self.source = source
        self.model = model
        self.now_time = datetime.now().strftime('%Y%m%d %H:%M:%S')
        self.file_name = ''

    def parser(self, input_path, output_path, mode='w'):
        f = open(input_path, 'r')
        # 样本换成列表
        sample_buff_list = []
        # 按行读文件
        for line in tqdm(f.readlines()):
            # 解析样本
            sample_buff_list += self.line_parser(json.loads(line))
            # 写入样本
            if len(sample_buff_list) > 20000:
                self.output(sample_buff_list, output_path, mode)
                sample_buff_list = []
        f.close()
        # 剩余样本写入
        self.output(sample_buff_list, output_path, mode)

    def json_parser(self, input_path, output_path, mode='w'):
        # 样本换成列表
        # json.load(input_path) 报错
        f = open(input_path, 'r')
        # 解析样本
        sample_buff_list = self.line_parser(json.loads(''.join(f.readlines())))
        f.close()
        # 写入样本
        self.output(sample_buff_list, output_path, mode)

    def line_parser(self, json_text):
        # 获取问答部分内容
        meta_instruction = json_text.get('meta_instruction')
        num_turns = json_text.get('num_turns')
        chat = json_text.get('chat')
        qa_list = []
        for chat_index in range(num_turns):
            plain_text = chat['turn_{}'.format(chat_index + 1)]
            question = plain_text['Human'].replace('<eoh>\n', '').replace('<|Human|>: ', '')
            answer = plain_text['MOSS'].replace('<eom>\n', '').replace('<|MOSS|>: ', '')
            # 样本列表
            qa_list.append({
                'id': get_hashid('{}_{}_{}'.format(self.source, question, answer)),
                '问': question,
                '答': answer,
                '来源': self.source,
                '元数据': {
                    'create_time': self.now_time,
                    '问题明细': "\"from\": \"human\"",  # 当前硬编码，可能需要改为提取方式
                    '回答明细': "\"from\": \"moss\"",
                    '扩展字段': json.dumps({
                        "会话": chat_index + 1,  # qa_id,
                        "多轮序号": chat_index + 1,
                        "解析模型": self.model,
                        "meta_instruction": meta_instruction,
                        "原始文件名": self.file_name,
                    }, ensure_ascii=False)
                }
            })

        return qa_list

    def proc(self, content):
        content = content.replace('<eoh>\n', '').replace('<|Human|>: ', '')
        content = content.replace('<eom>\n', '').replace('<|MOSS|>: ', '')
        # content = re.sub(r'\[MOSS\]:|\[Human\]:|<eoa>|<eoh>', '', content)
        content = content.strip()
        return content

    def output(self, qa_list, output_path, mode='w'):
        f = open(output_path, mode)
        for qa_sample in qa_list:
            f.write(json.dumps(qa_sample, ensure_ascii=False) + '\n')
        f.close()


if __name__ == '__main__':
    # 数据根目录
    root = 'data/moss-003-sft-plugin-data/conversation_with_plugins'
    # 模型
    model = 'MOSS'
    source = 'moss-002-sft-data'
    # 加载解析工具
    qa_parser = QAParser(source, model)
    # 待解析的文件列表
    folder_list = [
        'calculator',
        'equation_solver',
        'mix',
        'text2img',
        'web_search',
    ]
    # 文件夹路径
    folder_list = [os.path.join(root, folder) for folder in folder_list]

    # 输出文件路径
    output_path = 'data/sample/moss-003-sft-data-plugin.json'

    for folder in folder_list:
        for file_name in os.listdir(folder):
            # 文件
            qa_parser.file_name = os.path.basename(file_name)
            # 文件路径拼接
            input_path = os.path.join(folder, file_name)
            # 批量解析
            qa_parser.json_parser(input_path, output_path, mode='a')
