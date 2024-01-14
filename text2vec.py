import os
import torch
from functional import seq
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch.nn.functional as F  
from torch import cosine_similarity
from config import Config

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"



class TextVector():
    def __init__(self,cfg):
        self.bert_path = cfg.bert_path
        self.load_model()

    def load_model(self):
        """载入模型"""
        self.tokenizer = AutoTokenizer.from_pretrained(self.bert_path)
        self.model = AutoModel.from_pretrained(self.bert_path)


    def mean_pooling(self, model_output, attention_mask):
        """采用序列mean-pooling获得句子的表征向量"""
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def get_vec(self, sentences):
        """通过模型获取句子的向量"""
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        sentence_embeddings = sentence_embeddings.data.cpu().numpy().tolist()
        return sentence_embeddings

    def get_vec_bath(self,data, bs):
        """batch方式获取，提高效率"""
        data = seq(data).grouped(bs)
        all_vectors = []
        for batch in data:
            vecs = self.get_vec(batch)
            all_vectors.extend(vecs)
        all_vectors = torch.tensor(np.array(all_vectors))
        return all_vectors

    def vector_similarity(self, vectors):
        """以[query，text1，text2...]来计算query与text1，text2,...的cosine相似度"""
        vectors = F.normalize(vectors, p=2, dim=1)
        q_vec = vectors[0,:]
        o_vec = vectors[1:,:]
        sim = cosine_similarity(q_vec, o_vec)
        sim = sim.data.cpu().numpy().tolist()
        return sim

cfg = Config()
tv = TextVector(cfg)
get_vector = tv.get_vec_bath
get_sim = tv.vector_similarity


