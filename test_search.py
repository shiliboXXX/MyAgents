# test_advanced_search.py
import sys
import os
from dotenv import load_dotenv

from tools.builtin.search_tool import SearchTool
from tools import ToolRegistry

# 加载环境变量
load_dotenv()


def test_api_configuration():
    """测试API配置检查"""
    print("🔧 测试API配置检查:")

    # 直接创建搜索工具实例
    search_tool = SearchTool()

    # 如果没有配置API，会显示配置提示
    result = search_tool.run({"input": "机器学习算法"})
    print(f"搜索结果: {result}")

def test_with_agent():
    """测试与Agent的集成"""
    print("\n🤖 与Agent集成测试:")
    print("高级搜索工具已准备就绪，可以与Agent集成使用")

    # 显示工具描述
    registry = ToolRegistry()
    tools_desc = registry.get_tools_description()
    print(f"工具描述:\n{tools_desc}")

if __name__ == "__main__":
    test_api_configuration()
    test_with_agent()