# MossQA-mnbvc

## 项目描述
- 本项目主要对开源的Moss stf数据进行整理 ，转换成mnbvc多轮对话格式
- 各个数据集原始的数据格式见 dataset
- 处理结果为 jsonl，每行对应一条数据

## 环境
python3.8

## 数据源
+ [moss-002-sft-data](https://huggingface.co/datasets/fnlp/moss-002-sft-data): MOSS-002所使用的多轮对话数据，覆盖有用性、忠实性、无害性三个层面，包含由text-davinci-003生成的约57万条英文对话和59万条中文对话。
+ [moss-003-sft-data](https://github.com/OpenLMLab/MOSS/tree/main/SFT_data): moss-moon-003-sft所使用的多轮对话数据，基于MOSS-002内测阶段采集的约10万用户输入数据和gpt-3.5-turbo构造而成，相比moss-002-sft-data，moss-003-sft-data更加符合真实用户意图分布，包含更细粒度的有用性类别标记、更广泛的无害性数据和更长对话轮数，约含110万条对话数据。完整数据已全部开源。
+ [moss-003-sft-plugin-data](https://github.com/OpenLMLab/MOSS/tree/main/SFT_data/conversations/conversation_with_plugins): moss-moon-003-sft-plugin所使用的插件增强的多轮对话数据，包含支持搜索引擎、文生图、计算器、解方程等四个插件在内的约30万条多轮对话数据。已开源除text2image之外的所有数据。
+ moss-003-pm-data: moss-moon-003-pm所使用的偏好数据，包含在约18万额外对话上下文数据及使用moss-moon-003-sft所产生的回复数据上构造得到的偏好对比数据，将在近期开源。

## 用法
1. 下载数据到 data 目录下(各个数据源下载后的数据格式参考dataset目录下的sample文件)
2. 运行对应的处理脚本

`data/`
```python
.
├── moss-002-sft-data
├── moss-003-sft-data
├── moss-003-sft-plugin-data
└── sample

```


## 代码说明
```
python sft2.py
```

| 数据路径                   | 运行脚本           | 结果输出                                      |
|------------------------|----------------|-------------------------------------------|
| data/moss-002-sft-data | python sft2.py | data/sample/moss-002-sft-data.json        |
| data/moss-003-sft-data | python sft3.py | data/sample/moss-003-sft-data.json        |
| data/moss-003-sft-plugin-data |  python sft3-plugin.py              | data/sample/moss-003-sft-data-plugin.json |


## 结果示例
1. moss-002-sft-data.json

```json
{
  "id": "f6a974de0fd25ee7ebdcc17de4d237e9",
  "问": "介绍亚马逊雨林的特征",
  "答": "亚马逊雨林是地球上最大的雨林，位于南美洲的亚马逊河流域。它的特征包括：1. 占地面积约5.5万平方公里，覆盖了南美洲的九个国家和地区；2. 雨林中有大量的动植物种，其中约有40万种植物、3万种脊椎动物；3. 大自然的废弃物可以被有效利用，例如水果和木材；4. 它是全球气候系统的重要组成部分，能够帮助减少温室气体排放量",
  "来源": "moss-002-sft-data",
  "元数据": {
    "create_time": "20231118 13:47:38",
    "问题明细": "\"from\": \"human\"",
    "回答明细": "\"from\": \"moss\"",
    "扩展字段": "{\"会话\": 1, \"多轮序号\": 1, \"解析模型\": \"MOSS\", \"prefix\": \"MOSS is an AI assistant developed by the FudanNLP Lab and Shanghai AI Lab. Below is a conversation between MOSS and human.\", \"原始文件名\": \"zh_helpfulness.json\"}"
  }
}
```


## 多轮对话语料

[格式检查工具](https://github.com/X94521/DataCheck_MNBVC)



## 下载工具代码
```python
 git clone https://github.com/X94521/DataCheck_MNBVC.git
```

`MossQA-mnbvc`
```
.
├── DataCheck_MNBVC
├── README.md
├── data
├── sft2.py
├── sft3-plugin.py
└── sft3.py
```

## 格式检查
```python
cd DataCheck_MNBVC
python check_data.py --dataset ../data/sample/moss-003-sft-data-plugin.json
```


| 数据路径                   | 运行脚本           | 结果输出                                      | 格式校验结果                                                                                                                                                                                                         |
|------------------------|----------------|-------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| data/moss-002-sft-data | python sft2.py | data/sample/moss-002-sft-data.json        | checking dataset: ../data/sample/moss-002-sft-data.json the type of dataset moss-002-sft-data.json is 多轮对话/问答语料数据 check dataset moss-002-sft-data.json finished, right line 3534988 / total check line 3534988 |
| data/moss-003-sft-data | python sft3.py | data/sample/moss-003-sft-data.json        | the type of dataset moss-003-sft-data.json is 多轮对话/问答语料数据 check dataset moss-003-sft-data.json finished, right line 6234056 / total check line 6234056 checking dataset: ../data/sample/moss-002-sft-data.json |
| data/moss-003-sft-plugin-data |  python sft3-plugin.py              | data/sample/moss-003-sft-data-plugin.json | the type of dataset moss-003-sft-data-plugin.json is 多轮对话/问答语料数据 check dataset moss-003-sft-data-plugin.json finished, right line 950 / total check line 950                                                   |


[moss-sft处理后数据下载](https://1drv.ms/f/s!AuPutNFHzxWBkVQ4ADmT-1GRlW6c?e=8zAp88)