import os
import numpy as np

from lonia.utils import get_config_yaml, normalize, normalize_df

__mapping__ = {
    'macro_news': 'MACRO_NEWS', 
    'international_news': 'INTERNATIONAL_NEWS', 
    'stock_market': 'VN_STOCK_MARKET', 
    'banking': 'BANKING', 
    'oil_and_gas': 'OIL_AND_GAS'
}

class TFRanking(object):
    def __init__(self, config_file: str=None):
        """Initialize a TFRanking object

        :param config_file: (str) Path to the config file, that define keywords in sub category.
        """
        
        self.config = None
        if config_file:
            config = get_config_yaml(config_file=config_file)
            self.config = config

    def get_rank(self, sample: str, prior_category: str):
        """Function to get the rank of news (the order of priority to displayed on the home page. 
        
        :param sample: (str) The sample get rank
        :param prior_category: (str) The category of news is categorized before ranking
        """
        if prior_category not in __mapping__:
            print(f"Warning: `prior_category` not in catebogry must be ranking. ")
            return 1

        sample = normalize(text=sample, lowercase=True, rm_emoji=True, rm_special_characters=True, rm_url=True)

        self.data = self.config.get(__mapping__[prior_category], None)
        self.num_ranking = len(self.data)

        bowCount = len(sample.split(' '))

        output = {}
        for rank, values in self.data.items():
            output[rank] = 0
            keywords = values.get('keywords', None)

            for kw in keywords:
                temp = sample.count(kw.lower())
                temp = temp/bowCount

                output[rank] += temp
        
        ## Get MAX_SCORE and return Rank
        MAX_SCORE = 0
        RANK = self.num_ranking
        for k, v in output.items():
            if v > MAX_SCORE:
                RANK = k
                MAX_SCORE = v
        
        return {
            'rank': int(RANK), 
            'score': MAX_SCORE, 
            'name_rank': self.data[RANK].get('name', None)
        }


class RuleRanking(object):
    def __init__(self, config_file: str=None):
        """Initialize a Rule-based Ranking object

        :param config_file: (str) Path to the config file, that define keywords in sub category.
        """
        
        self.config = None
        if config_file:
            config = get_config_yaml(config_file=config_file)
            self.config = config

    def get_rank(self, sample: str, prior_category: str):
        """Function to get the rank of news (the order of priority to displayed on the home page. 
        
        :param sample: (str) The sample get rank
        :param prior_category: (str) The category of news is categorized before ranking
        """
        if prior_category not in __mapping__:
            print(f"Warning: `prior_category` not in catebogry must be ranking. ")
            return 1

        sample = normalize(text=sample, lowercase=True, rm_emoji=True, rm_special_characters=True, rm_url=True)

        self.data = self.config.get(__mapping__[prior_category], None)
        self.num_ranking = len(self.data)
        
        RANK = self.num_ranking
        SCORE = 1
        for rank, values in self.data.items():
            keywords = values.get('keywords', None)

            for kw in keywords:
                if kw in sample:
                    RANK = rank
                    return {
                        'rank': int(RANK), 
                        'score': SCORE, 
                        'name_rank': self.data[RANK].get('name', None)
                    }
        
        return {
            'rank': int(RANK), 
            'score': SCORE, 
            'name_rank': self.data[RANK].get('name', None)
        }