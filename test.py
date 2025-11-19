# --- 客户端使用示例 ---
from dotenv import load_dotenv
from core.llm import MyAgentsLLM
load_dotenv()

from agent.simple_agent import SimpleAgent
from tools.registry import ToolRegistry
from tools.builtin.memory_tool import MemoryTool

def demo_simple_agent_with_memory():
    """演示1: SimpleAgent + MemoryTool - 智能记忆助手"""
    print("🧠 演示1: SimpleAgent + 记忆工具（自动工具调用）")
    print("=" * 50)

    # 创建LLM
    llm = MyAgentsLLM()

    # 创建记忆工具
    memory_tool = MemoryTool(
        user_id="demo_user_001",
        memory_types=["working"]
    )

    # 创建工具注册表
    tool_registry = ToolRegistry()
    tool_registry.register_tool(memory_tool)

    # 创建支持工具的SimpleAgent
    agent = SimpleAgent(
        name="记忆助手",
        llm=llm,
        tool_registry=tool_registry,
        system_prompt="""你是一个有记忆能力的AI助手。你能记住我们的对话历史和重要信息。

工具使用指南：
- 当用户提供个人信息时，使用 [TOOL_CALL:memory:store=信息内容] 存储
- 当需要回忆用户信息时，使用 [TOOL_CALL:memory:recall=查询关键词] 检索
- 当用户询问历史对话时，使用 [TOOL_CALL:memory:action=summary] 获取摘要

重要原则：
- 主动记录用户的重要信息（姓名、职业、兴趣等）
- 在回答时参考相关的历史记忆
- 提供个性化的建议和服务"""
    )

    print("💬 开始智能对话演示...")

    # 模拟多轮对话
    conversations = [
        "你好！我叫李明，是一名软件工程师，专门做Python开发",
        "我最近在学习机器学习，特别对深度学习感兴趣",
        "你能推荐一些Python机器学习的库吗？",
        "你还记得我的名字和职业吗？请结合我的背景给我一些学习建议"
    ]

    for i, user_input in enumerate(conversations, 1):
        print(f"\n--- 对话轮次 {i} ---")
        print(f"👤 用户: {user_input}")

        # SimpleAgent会自动使用memory工具
        response = agent.run(user_input)
        print(f"🤖 助手: {response}")

    # 显示记忆摘要
    print(f"\n📊 最终记忆系统状态:")
    summary = memory_tool.run({"action": "summary"})
    print(summary)

    return memory_tool

if __name__ == '__main__':
    demo_simple_agent_with_memory()


    # try:
    #     llmClient = MyAgentsLLM()
    #
    #     # 准备消息
    #     messages = [{"role": "user", "content": "你好，请介绍一下你自己。"}]
    #
    #     # 发起调用，think等方法都已从父类继承，无需重写
    #     response_stream = llmClient.think(messages)
    #
    #     # 打印响应
    #     print("ModelScope Response:")
    #     for chunk in response_stream:
    #         # chunk 已经是文本片段，可以直接使用
    #         print(chunk, end="", flush=True)
    #
    # except ValueError as e:
    #     print(e)