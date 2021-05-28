import os
import torch
import random
import pickle
import numpy as np
import pandas as pd

from pathlib import Path
from typing import Text, Any, Dict, Union, List
from transformers import AutoModel, AutoTokenizer
from sklearn.cluster import MiniBatchKMeans

from lonia.utils import normalize

seed_val = 17
random.seed(seed_val)
np.random.seed(seed_val)
torch.manual_seed(seed_val)
torch.cuda.manual_seed_all(seed_val)

class LoniaClustering:
    def __init__(self, model_path=None, pretrained='vinai/phobert-base', max_seq_length=256):
        self.pretrained = pretrained
        self.model_path = model_path
        self.max_seq_length = max_seq_length

        self.device = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.tokenizer = AutoTokenizer.from_pretrained(self.pretrained)
        self.embedder = AutoModel.from_pretrained(self.pretrained)
        if self.model_path:
            self.load(path=self.model_path)

    def encode(
        self, 
        sentence: str, 
        convert_to_numpy: bool = True, 
    ):

        sentence = normalize(sentence, lowercase=True, rm_emoji=True, rm_url=True, rm_special_characters=True)
        if len(sentence.split()) > self.max_seq_length-16:
            sentence = ' '.join(sentence.split()[:self.max_seq_length-16])
            
        input_ids = torch.tensor([self.tokenizer.encode(sentence)])

        with torch.no_grad():
            features = self.embedder(input_ids, return_dict=False)
            output_tokens = features[0]
            print(f"output_tokens: {output_tokens.size()} {output_tokens}")
            cls_tokens = output_tokens[:, 0, :]  # CLS token is first token

            if convert_to_numpy:
                cls_tokens = cls_tokens.detach().cpu().numpy()

        return cls_tokens[0]

    def train(
        self, 
        data_path: str=None, 
        text_col: str='content', 
        n_clusters: int=6, 
        model_dir: str='./models/clustering', 
        model_name: str='model.pkl', 
        is_normalize: bool=True, 
        n_samples: int=None, 
        **kwargs
    ):
        df = pd.read_csv(data_path, encoding='utf-8')
        if n_samples:
            df = df.sample(n=n_samples)

        self.corpus = []
        self.corpus = [sentence for sentence in df[text_col]]
        self.corpus_embeddings = [self.encode(sentence) for sentence in self.corpus]

        self.clustering_model = MiniBatchKMeans(n_clusters=n_clusters)
        self.clustering_model.fit(self.corpus_embeddings)
        # self.cluster_assignment = self.clustering_model.labels_.tolist()

        if not os.path.exists(model_dir):
            os.mkdir(model_dir)

        pickle.dump(self.clustering_model, open(f"{Path(model_dir)/model_name}", "wb"))
        print(f"Path to the saved model: {Path(model_dir)/model_name}")

        return df, self.corpus, self.corpus_embeddings

    def load(self, path):
        path = os.path.abspath(path)
        self.clustering_model = pickle.load(open(path, "rb"))

    def predict(
        self, 
        sample: Text, 
        label_dict: Dict=None
    ):
        features = self.encode(sample).reshape(1, -1).astype(np.float64)
        index = self.clustering_model.predict(features)
        
        if label_dict:
            return label_dict.get(index, index)
        return index