---
license: cc-by-4.0
task_categories:
- conversational
- text-generation
language:
- en
- zh
size_categories:
- 1M<n<10M
---

# Dataset Card for "moss-002-sft-data"

## Dataset Description

- **Homepage:** [https://txsun1997.github.io/blogs/moss.html](https://txsun1997.github.io/blogs/moss.html)
- **Repository:** [https://github.com/OpenLMLab/MOSS](https://github.com/OpenLMLab/MOSS)
- **Total amount of disk used:** 2.16 GB

### Dataset Summary

An open-source conversational dataset that was used to train MOSS-002. The user prompts are extended based on a small set of human-written seed prompts in a way similar to [Self-Instruct](https://arxiv.org/abs/2212.10560). The AI responses are generated using `text-davinci-003`. The user prompts of `en_harmlessness` are from [Anthropic red teaming data](https://github.com/anthropics/hh-rlhf/tree/master/red-team-attempts).

### Data Splits

| name                 | \# samples |
|----------------------|-----------:|
| en_helpfulness.json  | 419049     |
| en_honesty.json      | 112580     |
| en_harmlessness.json | 38873      |
| zh_helpfulness.json  | 447750     |
| zh_honesty.json      | 142885     |



```shell
.
├── README.md
├── en_harmlessness.json
├── en_helpfulness.json
├── en_honesty.json
├── gitattributes
├── zh_helpfulness.json
└── zh_honesty.json
```