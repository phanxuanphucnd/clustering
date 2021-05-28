import os
import re
import regex
import yaml 
import pandas as pd

from pandas import DataFrame
from typing import Any, Text
from unicodedata import normalize as nl
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report

def is_empty(text: Text) -> bool:
    return text is None or text == ''

def normalize(
    text: Text=None, 
    form: Text='NFKC', 
    lowercase: bool=True, 
    rm_url: bool=False, 
    rm_emoji: bool=False, 
    rm_special_characters: bool=False
) -> Any:
    """Function normalize text input. """
    if is_empty(text):
        return None

    text = nl(form, text).strip()
    
    # lowercase 
    if lowercase:
        text = text.lower().strip()
    
    # Remove emoji
    if rm_emoji:
        emoji_pattern = regex.compile("["
                                    u"\U0001F600-\U0001F64F"  # emoticons
                                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                    "]+", flags=regex.UNICODE)
        text = emoji_pattern.sub(r" ", text) 
    
    # Remove url, link
    if rm_url:
        url_regex = re.compile(r'\bhttps?://\S+\b')
        text = url_regex.sub(r" ", text)

    # Remove special token and duplicate <space> token
    if rm_special_characters:
        text = regex.sub(r"[^%$&a-z0-9A-Z*\sÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠẾếàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸýửữựỳỵỷỹ]", " ", text)
        text = regex.sub(r"\s{2,}", " ", text)

    return text

def normalize_df(
    data_df: DataFrame=None, 
    col: Text='text', 
    form: Text='NFKC', 
    lowercase: bool=True, 
    rm_url: bool=False, 
    rm_emoji: bool=False, 
    rm_special_characters: bool=False
) -> DataFrame:
    
    data_df[col] = data_df[col].apply(lambda x: normalize(
        x, form=form, lowercase=lowercase, rm_emoji=rm_emoji, rm_url=rm_url, rm_special_characters=rm_special_characters))
    
    return data_df


def get_config_yaml(config_file: str):
    """This function will parse the configuration file that was provided as a 
    system argument into a dictionary.

    :param config_file: Path to the config file

    :return: A dictionary contraining the parsed config file
    """
    if not isinstance(config_file, str):
        raise TypeError(f"The config must be a file path not {type(config_file)}")
    elif not os.path.isfile(config_file):
        raise FileNotFoundError(f"  File {config_file} is not found!")
    elif not config_file[-5:] == ".yaml":
        raise TypeError(f"We only support .yaml format")
    else:
        print(f"Load config-file from: {config_file}")
        
        with open(config_file, 'r') as file:
            cfg_parser = yaml.load(file, Loader=yaml.Loader)

    return cfg_parser
