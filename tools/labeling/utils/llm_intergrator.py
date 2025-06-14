import requests
import time

class LLMIntegrator:
    """
    DeepSeek LLM API集成，用于实体、关系、事件链抽取。
    需在环境变量或配置文件中设置DEEPSEEK_API_KEY。
    """
    API_URL = "https://api.deepseek.com/v1/chat/completions"

    @staticmethod
    def extract(text, task="entity_extraction", api_key=None, max_retries=3):
        """
        :param text: 输入文本
        :param task: 任务类型（entity_extraction/relation_extraction/event_chain）
        :param api_key: DeepSeek API Key
        :return: LLM抽取结构化结果
        """
        if api_key is None:
            import os
            api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("请设置DEEPSEEK_API_KEY环境变量或传入api_key参数")
        # 构造prompt
        prompt_map = {
            "entity_extraction": "请从下列史料文本中抽取所有历史人物、组织、地点、事件等实体，输出JSON数组，每项包含name、type、evidence。",
            "relation_extraction": "请从下列史料文本中抽取所有实体间的关系，输出JSON数组，每项包含subject、predicate、object、evidence。",
            "event_chain": "请从下列史料文本中梳理时序化事件链，输出JSON数组，每项包含event、participants、time、cause、result、evidence。"
        }
        prompt = prompt_map.get(task, prompt_map["entity_extraction"]) + "\n史料文本：" + text
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是历史知识抽取专家，输出结构化JSON。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1024
        }
        for attempt in range(max_retries):
            try:
                resp = requests.post(LLMIntegrator.API_URL, headers=headers, json=data, timeout=60)
                resp.raise_for_status()
                result = resp.json()
                # 解析LLM输出
                content = result['choices'][0]['message']['content']
                import json
                # 只提取第一个JSON对象
                json_start = content.find('[')
                json_end = content.rfind(']')
                if json_start != -1 and json_end != -1:
                    return json.loads(content[json_start:json_end+1])
                else:
                    return content
            except Exception as e:
                print(f"[WARN] LLM调用失败({attempt+1}/{max_retries})：{e}")
                time.sleep(2)
        raise RuntimeError("DeepSeek LLM抽取失败，请检查API Key和网络")
