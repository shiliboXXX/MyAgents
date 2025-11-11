# --- 客户端使用示例 ---
from dotenv import load_dotenv
from core.llm import MyAgentsLLM
load_dotenv()

if __name__ == '__main__':
    try:
        llmClient = MyAgentsLLM()
        
        # 准备消息
        messages = [{"role": "user", "content": "你好，请介绍一下你自己。"}]

        # 发起调用，think等方法都已从父类继承，无需重写
        response_stream = llmClient.think(messages)

        # 打印响应
        print("ModelScope Response:")
        for chunk in response_stream:
            # chunk 已经是文本片段，可以直接使用
            print(chunk, end="", flush=True)

    except ValueError as e:
        print(e)