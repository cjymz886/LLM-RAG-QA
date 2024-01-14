

class Config():

    #retrievor参数
    topd = 3    #召回文章的数量
    topt = 6    #召回文本片段的数量
    maxlen = 128  #召回文本片段的长度
    topk = 5    #query召回的关键词数量
    bert_path = r'E:\pretraing_models\torch\text2vec-base-chinese'
    recall_way = 'embed'  #召回方式 ,keyword,embed

    #generator参数
    model_name_or_path = r'E:\pretraing_models\torch\baichuan2-7B-Chat'  #llm模型位置
    max_source_length = 767  #输入的最大长度
    max_target_length = 256  #生成的最大长度
    model_max_length = 1024  #序列最大长度

