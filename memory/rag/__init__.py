"""RAG (检索增强生成) 模块

合并了 GraphRAG 能力：
- loader：文件加载/分块（含PDF、语言标注、去重）
- embedding/cache：嵌入与SQLite缓存，默认哈希回退
- vector search：Qdrant召回
- rank/merge：融合排序与片段合并
"""

# 说明：原先的 .embeddings 已合并到上级目录的 memory/embedding.py
# 这里做兼容导出，避免历史引用报错。
from memory.embedding import (
    EmbeddingModel,
    TFIDFEmbedding,
    create_embedding_model,
    create_embedding_model_with_fallback,
)

# 兼容旧类名（历史代码中可能从此处导入）
# LocalTransformerEmbedding 类已不存在，移除兼容别名

__all__ = [
    "EmbeddingModel",
    "TFIDFEmbedding",
    "create_embedding_model",
    "create_embedding_model_with_fallback"
]