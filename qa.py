from generator import *



if __name__=="__main__":
    cfg = Config()
    qg = QueryGenerate(cfg)
    q_generate = qg.generate
    q_chat = qg.chat
    
    
    # query = '东南大学的现任校长是谁？'
    # query = '叔本华信仰什么宗教？'
    query = '戊戌变法中创建了什么报纸？'
    # query = '华山派的开山鼻祖是谁？'
    # query = '家喻户晓的角色印第安纳·琼斯是由哪个演员扮演的？'
    # query = '有什么和"凿壁偷光"意思相近的词语？'

    ####LLM+RAG#####
    res = q_chat(query)
    print(res)

    ####LLM######
    print('-----------------分割线-----------')
    res = q_chat(query,use_retrievor=False)
    print(res)