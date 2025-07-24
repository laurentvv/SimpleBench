# Bench AI with Ollama/LMStudio

<div align="center">

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Bench AI Logo](https://img.shields.io/badge/Bench%20AI-LLM%20Benchmark%20Tool-blue)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

Bench AI 是一个轻量级且高效的工具，用于评估通过 [Ollama](https://ollama.com/) 和 LMStudio 运行的语言模型 (LLM) 的性能。它允许研究人员和开发人员在标准化的编程和推理任务上客观地比较不同的模型。

## 🎯 最新结果

- **评估准确率**：在 HumanEval 上检测到 63% 的正确答案
- **评估方法**：5 种互补方法（标准化、AST、AI）
- **可重现性**：跨执行的一致结果

## ✨ 特性

- 🚀 **易于使用** - 直观的命令行界面
- 🔄 **多数据集支持** - 兼容 HumanEval、CruxEval 和 Code-X-GLUE
- 📊 **高级评估** - 容忍格式、缩进和功能等价性差异
- 📈 **详细分析** - 包含性能分析脚本
- 🧩 **可扩展** - 易于适应不同类型的基准测试

## 🛠️ 先决条件

- Python 3.13.5 或更高版本
- 已安装并运行 [Ollama](https://ollama.com/)

## 📦 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/laurentvv/bench-ai-ollama-lmstudio.git
   cd bench-ai-ollama-lmstudio
   ```

2. 创建虚拟环境并安装依赖项：
   ```bash
   python -m venv venv
   source venv/bin/activate  # 在 Windows 上：venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🚀 运行基准测试

1. 确保 Ollama 正在运行。

2. 下载您要测试的模型：
   ```bash
   ollama pull qwen3:14b
   ```

3. 使用您选择的数据集运行基准测试：
   ```bash
   # 对于 HumanEval
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-openai-openai-humaneval.json
   
   # 对于 CruxEval
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-cruxeval-org-cruxeval.json
   
   # 对于 Code-X-GLUE
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-google-code-x-glue-ct-code-to-text.json
   ```

## 📊 使用 Weave 进行跟踪

Bench AI 与 [Weave](https://wandb.ai/site/weave) 集成，这是一个用于跟踪和可视化实验的强大工具。

### Weave 设置

1. **创建 Weave 账户**：访问 [Weave 网站](https://wandb.ai/site/weave) 并创建免费账户。

2. **连接到 Weave**：创建账户后，您可以通过 CLI 连接（此项目不需要，由 API 管理）。

### 在 SimpleBench 中使用 Weave

要启用 Weave 跟踪，在运行基准测试时使用 `--entity` 和 `--project` 选项：

```bash
python run_benchmark_production.py \
  --model_name=qwen3:14b \
  --dataset_source=sql-console-for-openai-openai-humaneval.json \
  --entity="your-weave-entity" \
  --project="project-name"
```

- `--entity`：您的 Weave 用户名或组织。
- `--project`：您要记录实验的项目名称。

评估结果，包括详细分数和模型预测，将自动发送到您的 Weave 项目，允许您：

- 比较不同模型的性能
- 分析预测错误
- 与团队分享结果

### 可用选项

| 选项 | 描述 | 默认值 |
|------|------|--------|
| `--model_name` | 要测试的 Ollama 模型名称 | qwen3:14b |
| `--dataset_source` | 数据集源文件路径 | ./sql-console-for-openai-openai-humaneval.json |
| `--dataset_type` | 数据集类型 (humaneval, cruxeval, code_x_glue) | 自动检测 |
| `--num_responses` | 多数投票的响应数量 | 1 |
| `--temp` | 模型温度 | 0.1 |
| `--max_tokens` | 生成的最大令牌数 | 2048 |
| `--top_p` | 模型的 top_p 值 | 0.95 |
| `--max_retries` | 错误时的最大重试次数 | 3 |
| `--custom_system_prompt` | 自定义系统提示 | 基于数据集的默认提示 |

## 📊 结果分析

`run_benchmark_production.py` 脚本自动显示详细的评估结果，包括：

- 评估的问题总数
- 正确答案的数量和百分比
- 总执行时间
- 按评估方法分解的正确答案：
  - **基本标准化**：清理后的精确匹配
  - **高级标准化**：智能缩进处理
  - **极端标准化**：删除空格和换行符
  - **AST 比较**：语法结构分析
  - **AI 等价性**：功能等价性检测

这些详细统计信息帮助您准确了解模型的性能和它生成的响应类型。

## 🧩 支持的数据集

Bench AI 原生支持几个流行的语言模型评估数据集：

### 📁 此仓库中包含的数据集

此仓库包含 **3 个数据集文件**，**每个 30 个问题**：

- **`sql-console-for-openai-openai-humaneval.json`** - HumanEval（30 个问题）
- **`sql-console-for-cruxeval-org-cruxeval.json`** - CruxEval（30 个问题）
- **`sql-console-for-google-code-x-glue-ct-code-to-text.json`** - Code-X-GLUE（30 个问题）

> 💡 **获取更多问题**，请查看 Hugging Face 上的完整数据集（下面的链接）

### HumanEval

[HumanEval](https://huggingface.co/datasets/openai/openai_humaneval) 是 OpenAI 用于评估代码生成能力的基准。它包含带有解决方案和测试的 Python 编程问题。

### CruxEval

[CruxEval](https://huggingface.co/datasets/cruxeval-org/cruxeval) 是一组旨在评估语言模型推理能力的编程问题。

### Code-X-GLUE

[CodeXGLUE](https://huggingface.co/datasets/google/code_x_glue_ct_code_to_text) 是 Google 用于各种代码相关任务的基准，包括从源代码生成描述。

## 🔧 自动数据集检测

Bench AI 根据文件名或其内容自动检测数据集类型。您也可以使用 `--dataset_type` 选项明确指定类型。

## 💯 高级评估

Bench AI 使用结合多种方法的高级评估方法来检测正确答案：

1. **基本标准化**：删除标签并标准化空格
2. **高级标准化**：智能处理缩进和换行符
3. **极端标准化**：删除所有空格和换行符以检测仅在格式上不同的答案
4. **AST 比较**：分析代码语法结构以检测结构等价性
5. **AI 评估**：使用语言模型检测功能等价性

这种方法允许更精确地检测正确答案，即使它们在风格、变量名或算法方法方面与预期解决方案不同。

## 🚀 即将推出的功能

- 支持本地模型的 LMStudio
- MBPP 数据集（主要基本 Python 问题）
- 用于可视化结果的 Web 界面
- 模型间自动比较

## 🤝 贡献

欢迎贡献！请随时开启 issue 或提交 pull request。

## 📄 许可证

此项目采用 MIT 许可证。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。