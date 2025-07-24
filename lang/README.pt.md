# Bench AI with Ollama/LMStudio

<div align="center">

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Bench AI Logo](https://img.shields.io/badge/Bench%20AI-LLM%20Benchmark%20Tool-blue)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

Bench AI é uma ferramenta leve e eficiente para avaliar o desempenho de modelos de linguagem (LLMs) executados via [Ollama](https://ollama.com/) e LMStudio. Permite que pesquisadores e desenvolvedores comparem objetivamente diferentes modelos em tarefas padronizadas de programação e raciocínio.

## 🎯 Resultados Recentes

- **Precisão de avaliação**: 63% de respostas corretas detectadas no HumanEval
- **Métodos de avaliação**: 5 abordagens complementares (normalização, AST, IA)
- **Reprodutibilidade**: Resultados consistentes entre execuções

## ✨ Características

- 🚀 **Fácil de usar** - Interface de linha de comando intuitiva
- 🔄 **Suporte multi-dataset** - Compatível com HumanEval, CruxEval e Code-X-GLUE
- 📊 **Avaliação avançada** - Tolera diferenças de formatação, indentação e equivalência funcional
- 📈 **Análise detalhada** - Scripts de análise de desempenho incluídos
- 🧩 **Extensível** - Fácil de adaptar para diferentes tipos de benchmarks

## 🛠️ Pré-requisitos

- Python 3.13.5 ou superior
- [Ollama](https://ollama.com/) instalado e em execução

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/laurentvv/bench-ai-ollama-lmstudio.git
   cd bench-ai-ollama-lmstudio
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🚀 Executando o benchmark

1. Certifique-se de que o Ollama está em execução.

2. Baixe o modelo que você quer testar:
   ```bash
   ollama pull qwen3:14b
   ```

3. Execute o benchmark com um dataset de sua escolha:
   ```bash
   # Para HumanEval
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-openai-openai-humaneval.json
   ```

## 📊 Rastreamento com Weave

Bench AI está integrado com [Weave](https://wandb.ai/site/weave), uma ferramenta poderosa para rastrear e visualizar seus experimentos.

## 🧩 Datasets Suportados

Este repositório contém **3 arquivos de datasets** com **30 perguntas cada**:

- **`sql-console-for-openai-openai-humaneval.json`** - HumanEval (30 perguntas)
- **`sql-console-for-cruxeval-org-cruxeval.json`** - CruxEval (30 perguntas)
- **`sql-console-for-google-code-x-glue-ct-code-to-text.json`** - Code-X-GLUE (30 perguntas)

## 💯 Avaliação Avançada

Bench AI usa uma abordagem de avaliação avançada que combina múltiplos métodos para detectar respostas corretas:

1. **Normalização básica**: Remove tags e normaliza espaços
2. **Normalização avançada**: Lida inteligentemente com indentação e quebras de linha
3. **Normalização extrema**: Remove todos os espaços e quebras de linha
4. **Comparação AST**: Analisa a estrutura sintática do código
5. **Avaliação por IA**: Usa um modelo de linguagem para detectar equivalência funcional

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.