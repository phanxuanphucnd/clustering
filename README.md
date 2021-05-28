### Table of contents

1. [Introduction](#introduction)
2. [How to use?](#how_to_use)
    - [Installation](#install)
    - [Example usage](#usage)


## <a name='introduction'></a>

Clustering Text Document using RoBERTa.

## <a name='how_to_use'></a>

### Installation <a name='install'></a>

    python setup.py bdist_wheel

    pip install dist/lonia-0.0.1-py3-none-any.whl

### Example usage <a name='usage'></a>

```python

from lonia.clustering import LoniaClustering

clustering = LoniaClustering(pretrained='vinai/phobert-large')
clustering.train(
    data_path='./data/data_012021.csv', 
    text_col='', 
    n_clusters=7, 
    model_dir='./models/clustering', 
    model_name='clustering.pkl'
    )

sample = """gdp Cùng trong ngày 10/1, 3 dự án đặc biệt quan trọng với sự phát triển kinh tế - xã hội của đất nước đã được khởi công và khánh thành. 
Theo Thủ tướng Nguyễn Xuân Phúc, với việc mở rộng, xây dựng thêm 2 tổ máy công suất 240 MW, nâng tổng công suất Nhà máy thủy điện Hòa Bình lên 2. 
"""

# ax = clustering.predict(sample)
# print(ax)


from lonia.ranking import TFRanking

ranking = TFRanking(config_file='./data/config_ranking.yaml')

out = ranking.get_rank(sample=sample, prior_category='macro_news')

print(out)

```
