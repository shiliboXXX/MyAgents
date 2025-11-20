# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a modular AI agent framework called "MyAgents" that provides a flexible architecture for building intelligent agents with memory, tools, and context management capabilities.

## Core Architecture

### Agent Hierarchy
- `core/agent.py`: Abstract base agent class with common functionality
- `agent/simple_agent.py`: Basic conversational agent with optional tool calling support
- `agent/react_agent.py`: ReAct-style agent implementation

### Memory System
The memory system is organized into three types:
- `memory/types/working.py`: Working memory for temporary information
- `memory/types/episodic.py`: Episodic memory for experiences and conversations
- `memory/types/semantic.py`: Semantic memory for facts and knowledge
- `memory/manager.py`: Unified memory management interface

### Tool System
- `tools/base.py`: Abstract tool base class
- `tools/registry.py`: Tool registration and discovery system
- `tools/builtin/`: Built-in tools (search, memory, RAG)

### Context Management
- `context/builder.py`: GSSC (Gather-Select-Structure-Compress) pipeline for context construction

## Key Components

### LLM Integration
- `core/llm.py`: MyAgentsLLM wrapper for various LLM providers
- `core/config.py`: Configuration management
- `core/message.py`: Message handling and history management

### Storage Backends
- `memory/storage/qdrant_store.py`: Vector database storage
- `memory/storage/neo4j_store.py`: Graph database storage
- `memory/storage/document_store.py`: Document storage

## Development Commands

### Running Tests
```bash
python test.py                    # Run main test/demo
python test_search.py            # Run search tool tests
python test_context.py           # Run context builder tests
```

### Environment Setup
- Copy `.env` file and configure API keys and database connections
- Ensure Python 3.8+ is installed
- Install required dependencies (check imports for specific packages)

## Configuration

The system uses environment variables for configuration:
- LLM settings (API key, model ID, base URL)
- Database connections (Qdrant, Neo4j)
- Embedding model configuration

## Testing the Framework

The main test file demonstrates:
1. SimpleAgent with MemoryTool for intelligent conversations
2. RAG tool integration for knowledge retrieval
3. Tool calling with custom parameter parsing

Run `python test.py` to see the complete demo of all features.

## Key Design Patterns

### Tool Registration
Tools are registered using the ToolRegistry system and can be dynamically loaded/unloaded from agents.

### Memory Types
Memory items are automatically classified into working, episodic, or semantic based on content analysis.

### Context Building
The GSSC pipeline systematically constructs context from multiple sources while respecting token budgets.

### Parameter Parsing
The SimpleAgent includes intelligent parameter parsing that supports multiple formats:
- JSON objects
- Key=value pairs
- Simple inference based on tool types

## Important Notes

- The framework supports both streaming and non-streaming LLM responses
- Memory includes automatic importance scoring and forgetting mechanisms
- Tools can be expanded into multiple sub-tools using the expandable pattern
- All storage backends are abstracted through interfaces for easy swapping