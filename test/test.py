# from lonia.clustering import LoniaClustering

# clustering = LoniaClustering(pretrained='vinai/phobert-large')
# clustering.train(
#     data_path='./data/data_dailynews_012021.csv', 
#     text_col='', 
#     n_clusters=7, 
#     model_dir='./models/clustering', 
#     model_name='dailynews_clustering.pkl'
#     )

# sample = """gdp Cùng trong ngày 10/1, 3 dự án đặc biệt quan trọng với sự phát triển kinh tế - xã hội của đất nước đã được khởi công và khánh thành. 
# Theo Thủ tướng Nguyễn Xuân Phúc, với việc mở rộng, xây dựng thêm 2 tổ máy công suất 240 MW, nâng tổng công suất Nhà máy thủy điện Hòa Bình lên 2. 
# 400 MW, bằng công suất Thủy điện Sơn La. Thủ tướng đề nghị các đơn vị phát huy truyền thống tốt đẹp, ý chí quyết tâm, tinh thần đoàn kết, vượt khó, 
# nỗ lực phấn đấu gdp hoàn thành trước thời hạn ít nhất nửa năm, đưa Nhà máy vào vận hành đầu năm 2023 để bổ sung nguồn điện quý giá cho đất nước, đồng thời 
# phải bảo đảm tuyệt đối an toàn, chất lượng, tuân thủ đúng các yêu cầu quy định. Hồ Chí Minh, Bộ Giao thông Vận tải tổ chức Lễ khánh thành giai đoạn 1 
# Dự án cải tạo, nâng cấp đường cất hạ cánh, đường lăn Cảng hàng không quốc tế Tân Sơn Nhất và Dự án cải tạo, nâng cấp đường cất hạ cánh, đường lăn Cảng 
# hàng không quốc tế Nội Bài. Sáng 11/1, Bộ Giao thông vận tải, TP Đà Nẵng, tỉnh Thừa Thiên-Huế và Công ty Cổ phần Tập đoàn Đèo Cả đã khánh thành, đưa vào 
# khai thác hầm Hải Vân 2 dài hơn 6,2 km, là hầm đường bộ dài nhất Đông Nam Á. Hầm Hải Vân 2 được khởi công tháng 4/2016, gồm 2 giai đoạn. lạm phát qua xuất 
# khẩu
# nhập khẩu xuất khẩu import export  nhập siêu nhé
# """

# # ax = clustering.predict(sample)
# # print(ax)


# from lonia.ranking import TFRanking

# ranking = TFRanking(config_file='./data/config_ranking.yaml')

# out = ranking.get_rank(sample=sample, prior_category='macro_news')

# print(out)


import json

with open('./data/stock_code.json') as json_file:
    data = json.load(json_file)

from pprint import pprint
pprint(data)