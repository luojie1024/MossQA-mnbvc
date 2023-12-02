#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2023/11/18 09:52 
# @Author  : Roger 
# @Version : V 0.1
# @Email   : 550997728@qq.com
# @File    : main.py
import re
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
        for line in f.readlines():
            # 按list逐条解析
            json_text_list = json.loads(line)
            for line in tqdm(json_text_list):
                # 解析样本
                sample_buff_list += self.line_parser(line)
                # 写入样本
                if len(sample_buff_list) > 20000:
                    self.output(sample_buff_list, output_path, mode)
                    sample_buff_list = []
        # 剩余样本写入
        self.output(sample_buff_list, output_path, mode)

    def line_parser(self, json_text):
        # 获取问答部分内容
        plain_text = json_text.get('plain_text')
        prefix = json_text.get('prefix')
        # 样本id
        qa_id = get_hashid(plain_text)
        # 文本内容为空
        if not plain_text or len(plain_text) == 0:
            return []
        # 切分QA list
        qa_list = [text.split('<eoh>') for text in plain_text.split('<eoa>')]
        # 清理清洗
        qa_list = [(self.proc(qa_pair[0]),
                    self.proc(qa_pair[1])) for qa_pair in qa_list if len(qa_pair) == 2]
        # 样本列表
        qa_list = [{
            'id': get_hashid('{}_{}_{}'.format(self.source, question, answer)),
            '问': question,
            '答': answer,
            '来源': self.source,
            '元数据': {
                'create_time': self.now_time,
                '问题明细': "\"from\": \"human\"",  # 当前硬编码，可能需要改为提取方式
                '回答明细': "\"from\": \"moss\"",
                '扩展字段': json.dumps({
                    "会话": index + 1,  # qa_id,
                    "多轮序号": index + 1,
                    "解析模型": self.model,
                    "prefix": prefix,
                    "原始文件名": self.file_name,
                }, ensure_ascii=False)
            }

        } for index, (question, answer) in enumerate(qa_list)]

        return qa_list

    def proc(self, content):
        content = re.sub(r'\[MOSS\]:|\[Human\]:|<eoa>|<eoh>', '', content)
        content = content.strip()
        return content

    def output(self, qa_list, output_path, mode='w'):
        f = open(output_path, mode)
        for qa_sample in qa_list:
            f.write(json.dumps(qa_sample, ensure_ascii=False) + '\n')
        f.close()


if __name__ == '__main__':
    # 模型
    model = 'MOSS'
    source = 'moss-002-sft-data'
    # 加载解析工具
    qa_parser = QAParser(source, model)
    # 待解析的文件列表
    files = [
        'zh_helpfulness.json',
        'zh_honesty.json',
        'en_harmlessness.json',
        'en_helpfulness.json',
        'en_honesty.json',
    ]
    # 输出文件路径
    output_path = 'data/sample/moss-002-sft-data.json'

    # f = open('data/moss-003-sft-data/moss-003-sft-no-tools.jsonl', 'r')
    # lines = f.readlines()
    # line = json.loads(lines[0])

    for file_name in files:
        qa_parser.file_name = file_name
        input_path = 'data/moss-002-sft-data/{}'.format(file_name)
        # 批量解析
        qa_parser.parser(input_path, output_path, mode='a')


    # f = open('data/moss-003-sft-data/moss-003-sft-no-tools.jsonl', 'r')
    # lines=f.readline()
    # len(lines)