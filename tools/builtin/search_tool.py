"""搜索工具 - MyAgents 原生搜索实现。"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Iterable, List

import requests

from ..base import Tool, ToolParameter

try:  # 可选依赖，缺失时降级能力
    from markdownify import markdownify
except Exception:  # pragma: no cover - 可选依赖
    markdownify = None  # type: ignore

try:
    from ddgs import DDGS  # type: ignore
except Exception:  # pragma: no cover - 可选依赖
    DDGS = None  # type: ignore

try:
    from serpapi import GoogleSearch  # type: ignore
except Exception:  # pragma: no cover - 可选依赖
    GoogleSearch = None  # type: ignore

logger = logging.getLogger(__name__)

CHARS_PER_TOKEN = 4
DEFAULT_MAX_RESULTS = 5
SUPPORTED_RETURN_MODES = {"text", "structured", "json", "dict"}


def _limit_text(text: str, token_limit: int) -> str:
    char_limit = token_limit * CHARS_PER_TOKEN
    if len(text) <= char_limit:
        return text
    return text[:char_limit] + "... [truncated]"


def _fetch_raw_content(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as exc:  # pragma: no cover - 网络环境不稳定
        logger.debug("Failed to fetch raw content for %s: %s", url, exc)
        return None

    if markdownify is not None:
        try:
            return markdownify(response.text)  # type: ignore[arg-type]
        except Exception as exc:  # pragma: no cover - 可选依赖失败
            logger.debug("markdownify failed for %s: %s", url, exc)
    return response.text


def _normalized_result(
    *,
    title: str,
    url: str,
    content: str,
    raw_content: str | None,
) -> Dict[str, str]:
    payload: Dict[str, str] = {
        "title": title or url,
        "url": url,
        "content": content or "",
    }
    if raw_content is not None:
        payload["raw_content"] = raw_content
    return payload


def _structured_payload(
    results: Iterable[Dict[str, Any]],
    *,

    answer: str | None = None,
    notices: Iterable[str] | None = None,
) -> Dict[str, Any]:
    return {
        "results": list(results),
        "answer": answer,
        "notices": list(notices or []),
    }


class SearchTool(Tool):
    """支持多后端、可返回结构化结果的搜索工具。"""

    def __init__(
        self,
        tavily_key: str | None = None,
        serpapi_key: str | None = None,
        perplexity_key: str | None = None,
    ) -> None:
        super().__init__(
            name="search",
            description=(
                "智能网页搜索引擎，支持 SerpApi，可返回结构化或文本化的搜索结果。"
            ),
        )
        self.serpapi_key = serpapi_key or os.getenv("SERPAPI_API_KEY")

        self.available_backends: list[str] = []
        self.tavily_client = None
        self._setup_backends()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self, parameters: Dict[str, Any]) -> str | Dict[str, Any]:  # type: ignore[override]
        query = (parameters.get("input") or parameters.get("query") or "").strip()
        if not query:
            return "错误：搜索查询不能为空"

        mode = str(
            parameters.get("mode")
            or parameters.get("return_mode")
            or "text"
        ).lower()
        if mode not in SUPPORTED_RETURN_MODES:
            mode = "text"

        fetch_full_page = bool(parameters.get("fetch_full_page", False))
        max_results = int(parameters.get("max_results", DEFAULT_MAX_RESULTS))
        max_tokens = int(parameters.get("max_tokens_per_source", 2000))
        loop_count = int(parameters.get("loop_count", 0))

        payload = self._structured_search(
            query=query,
            fetch_full_page=fetch_full_page,
            max_results=max_results,
            max_tokens=max_tokens,
            loop_count=loop_count,
        )

        if mode in {"structured", "json", "dict"}:
            return payload

        return self._format_text_response(query=query, payload=payload)

    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="input",
                type="string",
                description="搜索查询关键词",
                required=True,
            ),
        ]

    def _setup_backends(self) -> None:
        if self.serpapi_key:
            if GoogleSearch is not None:
                self.available_backends.append("serpapi")
                print("✅ SerpApi 搜索引擎已初始化")
            else:
                print("⚠️ 未安装 google-search-results，无法使用 SerpApi 搜索")
        else:
            print("⚠️ SERPAPI_API_KEY 未设置")

    def _structured_search(
        self,
        *,
        query: str,
        fetch_full_page: bool,
        max_results: int,
        max_tokens: int,
        loop_count: int,
    ) -> Dict[str, Any]:
         return self._search_serpapi(
                query=query,
                fetch_full_page=fetch_full_page,
                max_results=max_results,
                max_tokens=max_tokens,
            )

    def _search_serpapi(
        self,
        *,
        query: str,
        fetch_full_page: bool,
        max_results: int,
        max_tokens: int,
    ) -> Dict[str, Any]:
        if not self.serpapi_key:
            raise RuntimeError("SERPAPI_API_KEY 未配置，无法使用 SerpApi 搜索")
        if GoogleSearch is None:
            raise RuntimeError("未安装 google-search-results，无法使用 SerpApi")

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.serpapi_key,
            "gl": "cn",
            "hl": "zh-cn",
            "num": max_results,
        }

        response = GoogleSearch(params).get_dict()

        answer_box = response.get("answer_box") or {}
        answer = answer_box.get("answer") or answer_box.get("snippet")

        results = []
        for item in response.get("organic_results", [])[:max_results]:
            raw_content = item.get("snippet")
            if raw_content and fetch_full_page:
                raw_content = _limit_text(raw_content, max_tokens)
            results.append(
                _normalized_result(
                    title=item.get("title") or item.get("link", ""),
                    url=item.get("link", ""),
                    content=item.get("snippet") or "",
                    raw_content=raw_content,
                )
            )

        return _structured_payload(results, answer=answer)

    def _format_text_response(self, *, query: str, payload: Dict[str, Any]) -> str:
        answer = payload.get("answer")
        notices = payload.get("notices") or []
        results = payload.get("results") or []

        lines = [f"🔍 搜索关键词：{query}", f"🧭 使用搜索源：google"]
        if answer:
            lines.append(f"💡 直接答案：{answer}")

        if results:
            lines.append("")
            lines.append("📚 参考来源：")
            for idx, item in enumerate(results, start=1):
                title = item.get("title") or item.get("url", "")
                lines.append(f"[{idx}] {title}")
                if item.get("content"):
                    lines.append(f"    {item['content']}")
                if item.get("url"):
                    lines.append(f"    来源: {item['url']}")
                lines.append("")
        else:
            lines.append("❌ 未找到相关搜索结果。")

        if notices:
            lines.append("⚠️ 注意事项：")
            for notice in notices:
                if notice:
                    lines.append(f"- {notice}")

        return "\n".join(line for line in lines if line is not None)


# 便捷函数
def search(query: str) -> str:
    tool = SearchTool()
    return tool.run({"input": query}) 
