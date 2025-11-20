# --- 客户端使用示例 ---
from dotenv import load_dotenv
from core.llm import MyAgentsLLM
load_dotenv()

from agent.simple_agent import SimpleAgent
from tools.registry import ToolRegistry
from tools.builtin.memory_tool import MemoryTool
from tools.builtin.rag_tool import RAGTool

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

def demo_simple_agent_with_rag():
    """演示2: SimpleAgent + RAGTool - 智能知识助手"""
    print("\n\n🔍 演示2: SimpleAgent + RAG工具（自动工具调用）")
    print("=" * 50)

    # 创建LLM
    llm = MyAgentsLLM()

    # 创建RAG工具 - 使用本地嵌入（推荐）
    rag_tool = RAGTool(
        knowledge_base_path="./demo_knowledge_base"
    )

    # 创建工具注册表
    tool_registry = ToolRegistry()
    tool_registry.register_tool(rag_tool)

    # 创建支持工具的SimpleAgent
    agent = SimpleAgent(
        name="知识助手",
        llm=llm,
        tool_registry=tool_registry,
        system_prompt="""你是一个专业的知识助手，可以从知识库中检索准确信息。

工具使用指南：
- 当用户询问技术问题时，使用 [TOOL_CALL:rag:search=关键词] 搜索知识库
- 基于检索到的信息提供准确回答
- 如果知识库中没有相关信息，诚实告知用户

工作流程：
1. 分析用户问题，提取关键词
2. 搜索知识库获取相关信息
3. 基于搜索结果给出专业回答"""
    )

    print("📚 正在构建知识库...")

    # 添加技术知识到RAG系统
    knowledge_items = [
        ("Python是一种高级编程语言，由Guido van Rossum在1989年开始开发，1991年首次发布。Python以其简洁的语法和强大的功能而闻名，广泛应用于Web开发、数据科学、人工智能等领域。", "python_intro"),
        ("机器学习是人工智能的一个分支，它使计算机能够在没有明确编程的情况下学习和改进。主要包括监督学习、无监督学习和强化学习三种类型。常用的Python机器学习库包括scikit-learn、pandas、numpy等。", "ml_basics"),
        ("深度学习是机器学习的一个子集，使用多层神经网络来模拟人脑的工作方式。深度学习在图像识别、自然语言处理、语音识别等领域取得了突破性进展。主要的深度学习框架包括TensorFlow、PyTorch、Keras等。", "deep_learning"),
        ("自然语言处理(NLP)是人工智能的一个重要分支，专注于计算机与人类语言之间的交互。NLP的主要任务包括文本分类、情感分析、机器翻译、问答系统等。常用的Python NLP库包括NLTK、spaCy、transformers等。", "nlp_intro")
    ]

    for content, doc_id in knowledge_items:
        result = rag_tool.run({"action": "add_text", "text": content, "document_id": doc_id})
        print(f"  ✅ 已添加: {doc_id}")

    print(f"\n📊 知识库统计:")
    stats = rag_tool.run({"action": "stats"})
    print(stats)

    # 测试智能问答
    queries = [
        "Python是什么时候发明的？谁发明的？",
        "什么是深度学习？它和机器学习有什么关系？",
        "推荐一些Python机器学习的库",
        "什么是量子计算？"  # 知识库中没有的信息
    ]

    print(f"\n💬 开始智能问答演示...")

    for i, query in enumerate(queries, 1):
        print(f"\n--- 查询 {i} ---")
        print(f"👤 用户: {query}")

        # SimpleAgent会自动使用RAG工具搜索并回答
        response = agent.run(query)
        print(f"🤖 助手: {response}")

    return rag_tool

if __name__ == '__main__':
    # demo_simple_agent_with_memory()
    demo_simple_agent_with_rag()


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