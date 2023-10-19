# Copyright (c) Alibaba, Inc. and its affiliates.
import unittest

import torch

from modelscope.pipelines.nlp.llm_pipeline import LLMPipeline
from modelscope.utils.test_utils import test_level


class LLMPipelineTest(unittest.TestCase):

    def setUp(self) -> None:
        self.messages_zh = {
            'messages': [{
                'role': 'user',
                'content': 'Hello! 你是谁？'
            }, {
                'role': 'assistant',
                'content': '我是你的助手。'
            }, {
                'role': 'user',
                'content': '你叫什么名字？'
            }]
        }
        self.messages_zh_with_system = {
            'messages': [{
                'role': 'system',
                'content': '你是达摩院的生活助手机器人。'
            }, {
                'role': 'user',
                'content': '今天天气好吗？'
            }]
        }
        self.prompt_zh = '请介绍一下你自己'
        self.messages_en = {
            'messages': [{
                'role': 'system',
                'content': 'You are a helpful assistant.'
            }, {
                'role': 'user',
                'content': 'Hello! Where is the capital of Zhejiang?'
            }, {
                'role': 'assistant',
                'content': 'Hangzhou is the capital of Zhejiang.'
            }, {
                'role': 'user',
                'content': 'Tell me something about HangZhou?'
            }]
        }
        self.prompt_en = 'Tell me the capital of Zhejiang. '
        self.messages_code = {
            'messages': [{
                'role':
                'system',
                'content':
                'You are a helpful, respectful and honest assistant '
                'with a deep knowledge of code and software design. '
                'Always answer as helpfully as possible, while being safe. '
                'Your answers should not include any harmful, unethical, racist, '
                'sexist, toxic, dangerous, or illegal content. Please ensure that '
                'your responses are socially unbiased and positive in nature.\n\n'
                'If a question does not make any sense, or is not factually coherent, '
                'explain why instead of answering something not correct. '
                'If you don\'t know the answer to a question, '
                'please don\'t share false information.'
            }, {
                'role':
                'user',
                'content':
                'write a program to implement the quicksort in java'
            }]
        }
        self.prompt_code = 'import socket\n\ndef ping_exponential_backoff(host: str):'

        self.message_wizard_math = {
            'messages': [{
                'role':
                'system',
                'content':
                'Below is an instruction that describes a task. '
                'Write a response that appropriately completes the request.'
            }, {
                'role':
                'user',
                'content':
                'James decides to run 3 sprints 3 times a week. He runs 60 meters each sprint.'
                'How many total meters does he run a week?'
            }]
        }
        self.prompt_wizard_math = """"Below is an instruction that describes a task.
        Write a response that appropriately completes the request.\n\n
        ### Instruction:\nJames decides to run 3 sprints 3 times a week. He runs 60 meters each sprint.
        How many total meters does he run a week?\n\n
        ### Response:"""

        self.message_wizard_code = {
            'messages': [{
                'role':
                'system',
                'content':
                'Below is an instruction that describes a task.'
                'Write a response that appropriately completes the request.'
            }, {
                'role': 'user',
                'content': 'Write a Jave code to sum 1 to 10'
            }]
        }
        self.prompt_wizard_code = """"Below is an instruction that describes a task.
        Write a response that appropriately completes the request.\n\n
        ### Instruction:\nWrite a Jave code to sum 1 to 10\n\n
        ### Response:"""

        self.messages_mm = {
            'messages': [{
                'role': 'system',
                'content': '你是达摩院的生活助手机器人。'
            }, {
                'role':
                'user',
                'content': [
                    {
                        'image':
                        'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'
                    },
                    {
                        'text': '这是什么?'
                    },
                ]
            }]
        }
        self.gen_cfg = {'do_sample': True, 'max_length': 512}

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_chatglm2(self):
        pipe = LLMPipeline(model='ZhipuAI/chatglm2-6b', device_map='auto')
        print('messages: ', pipe(self.messages_zh, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_chatglm2int4(self):
        pipe = LLMPipeline(model='ZhipuAI/chatglm2-6b-int4')
        print('messages: ', pipe(self.messages_zh, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_chatglm232k(self):
        pipe = LLMPipeline(model='ZhipuAI/chatglm2-6b-32k', device_map='auto')
        print('messages: ', pipe(self.messages_zh, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_llama2(self):
        pipe = LLMPipeline(
            model='modelscope/Llama-2-7b-ms',
            torch_dtype=torch.float16,
            device_map='auto',
            ignore_file_pattern=[r'.+\.bin$'])
        print('messages: ', pipe(self.messages_en, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_en, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_llama2chat(self):
        pipe = LLMPipeline(
            model='modelscope/Llama-2-7b-chat-ms',
            revision='v1.0.2',
            torch_dtype=torch.float16,
            device_map='auto',
            ignore_file_pattern=[r'.+\.bin$'])
        print('messages: ', pipe(self.messages_en, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_en, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_codellama(self):
        pipe = LLMPipeline(
            model='AI-ModelScope/CodeLlama-7b-Instruct-hf',
            torch_dtype=torch.float16,
            device_map='auto',
            ignore_file_pattern=[r'.+\.bin$'])
        print('messages: ', pipe(self.messages_code, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_code, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_baichuan_7b(self):
        pipe = LLMPipeline(
            model='baichuan-inc/baichuan-7B',
            device_map='auto',
            torch_dtype=torch.float16)
        print('messages: ', pipe(self.messages_zh, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_baichuan_13b(self):
        pipe = LLMPipeline(
            model='baichuan-inc/Baichuan-13B-Base',
            device_map='auto',
            torch_dtype=torch.float16)
        print('messages: ', pipe(self.messages_zh, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_baichuan_13bchat(self):
        pipe = LLMPipeline(
            model='baichuan-inc/Baichuan-13B-Chat',
            device_map='auto',
            torch_dtype=torch.float16)
        print('messages: ', pipe(self.messages_zh, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_baichuan2_7b(self):
        pipe = LLMPipeline(
            model='baichuan-inc/Baichuan2-7B-Base',
            device_map='auto',
            torch_dtype=torch.float16)
        print('messages: ', pipe(self.messages_zh, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_baichuan2_7bchat(self):
        pipe = LLMPipeline(
            model='baichuan-inc/Baichuan2-7B-Chat',
            device_map='auto',
            torch_dtype=torch.float16)
        print('messages: ', pipe(self.messages_zh, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skip('Need bitsandbytes')
    def test_baichuan2_7bchat_int4(self):
        pipe = LLMPipeline(
            model='baichuan-inc/Baichuan2-7B-Chat-4bits',
            device_map='auto',
            torch_dtype=torch.float16)
        print('messages: ', pipe(self.messages_zh, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skip('Need bitsandbytes')
    def test_baichuan2_13bchat_int4(self):
        pipe = LLMPipeline(
            model='baichuan-inc/Baichuan2-13B-Chat-4bits',
            device_map='auto',
            torch_dtype=torch.float16)
        print('messages: ', pipe(self.messages_zh, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_wizardlm_13b(self):
        pipe = LLMPipeline(
            model='AI-ModelScope/WizardLM-13B-V1.2',
            device_map='auto',
            torch_dtype=torch.float16,
            format_messages='wizardlm')
        print('messages: ', pipe(self.messages_en, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_en, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_wizardmath(self):
        pipe = LLMPipeline(
            model='AI-ModelScope/WizardMath-7B-V1.0',
            device_map='auto',
            torch_dtype=torch.float16,
            format_messages='wizardcode')
        print('messages: ', pipe(self.message_wizard_math, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_wizard_math, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_wizardcode_13b(self):
        pipe = LLMPipeline(
            model='AI-ModelScope/WizardCoder-Python-13B-V1.0',
            device_map='auto',
            torch_dtype=torch.float16,
            format_messages='wizardcode')
        print('messages: ', pipe(self.message_wizard_code, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_wizard_code, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 0, 'skip test in current test level')
    def test_wizardcode_1b(self):
        pipe = LLMPipeline(
            model='AI-ModelScope/WizardCoder-1B-V1.0',
            device_map='auto',
            torch_dtype=torch.float16,
            format_messages='wizardcode')
        print('messages: ', pipe(self.message_wizard_code, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_wizard_code, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_qwen(self):
        pipe = LLMPipeline(model='qwen/Qwen-7B-Chat', device_map='auto')
        print('messages: ', pipe(self.messages_zh_with_system, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skip('Need optimum and auto-gptq')
    def test_qwen_int4(self):
        pipe = LLMPipeline(model='qwen/Qwen-7B-Chat-Int4', device_map='auto')
        print('messages: ', pipe(self.messages_zh_with_system, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_qwen_vl(self):
        pipe = LLMPipeline(model='qwen/Qwen-VL-Chat', device_map='auto')
        print('messages: ', pipe(self.messages_mm, **self.gen_cfg))
        print('prompt: ', pipe(self.prompt_zh, **self.gen_cfg))


if __name__ == '__main__':
    unittest.main()
