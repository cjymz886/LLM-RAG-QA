import os
import json
import time
import torch
import transformers
from transformers.generation.utils import GenerationConfig
from retrievor import q_searching
from config import Config

class QueryGenerate():
    def __init__(self, cfg):
        self.model_name_or_path = cfg.model_name_or_path
        self.max_source_length = cfg.max_source_length
        self.max_target_length = cfg.max_target_length
        self.model_max_length = cfg.model_max_length
        self.load_model()

    def load_model(self):
        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            self.model_name_or_path,
            trust_remote_code=True,
            cache_dir=None,
        )
        self.model.half().cuda()
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.model_name_or_path,
            use_fast=False,
            trust_remote_code=True,
            model_max_length=self.model_max_length,
            cache_dir=None,
        )
        self.model.generation_config = GenerationConfig.from_pretrained(self.model_name_or_path)
    
    def build_prompt(self,query,use_retrievor):
        if use_retrievor:
            bg_text = q_searching(query)
            #限制bg_text长度
            bg_text_len = self.max_source_length - len(query) - 30
            bg_text = bg_text[:bg_text_len]
            print("#####################bg_text###################")
            print(bg_text)
            print("#####################bg_text###################")
            prompt ="请参考下面的<背景信息>回答“{}”的问题，要求：直接回答问题，不必做过多解释。\n\n<背景信息>\n{}。".format(query,bg_text)
            return prompt
        else:
            return query
        
        
    def generate(self, query):
        self.model.eval()
        with torch.autocast("cuda"):
            prompt = self.build_prompt(query,use_retrievor=True)
            model_inputs = self.tokenizer([prompt], max_length=self.max_source_length, truncation=True,add_special_tokens=True)
            input_ids = torch.LongTensor(model_inputs['input_ids']).to('cuda')
            out = self.model.generate(
                input_ids=input_ids,
                max_new_tokens= self.max_target_length,
                do_sample=True,
                top_p=0.8,
                temperature=0.4,
                top_k=30,
                eos_token_id=self.tokenizer.eos_token_id,

            )
            out = out[:, input_ids.size()[-1]:]
            out_text = self.tokenizer.decode(out[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
        return out_text

    def chat(self,query,use_retrievor=True):
        prompt = self.build_prompt(query,use_retrievor)
        messages = []
        messages.append({"role": "user", "content": prompt})
        res = self.model.chat(self.tokenizer, messages)
        return res





    

