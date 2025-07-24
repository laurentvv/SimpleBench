# Bench AI with Ollama/LMStudio

<div align="center">

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Bench AI Logo](https://img.shields.io/badge/Bench%20AI-LLM%20Benchmark%20Tool-blue)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

Bench AI — это легкий и эффективный инструмент для оценки производительности языковых моделей (LLM), работающих через [Ollama](https://ollama.com/) и LMStudio. Он позволяет исследователям и разработчикам объективно сравнивать различные модели на стандартизированных задачах программирования и рассуждения.

## 🎯 Последние результаты

- **Точность оценки**: 63% правильных ответов обнаружено на HumanEval
- **Методы оценки**: 5 дополняющих подходов (нормализация, AST, ИИ)
- **Воспроизводимость**: Согласованные результаты между выполнениями

## ✨ Особенности

- 🚀 **Простота использования** - Интуитивный интерфейс командной строки
- 🔄 **Поддержка нескольких наборов данных** - Совместим с HumanEval, CruxEval и Code-X-GLUE
- 📊 **Продвинутая оценка** - Допускает различия в форматировании, отступах и функциональной эквивалентности
- 📈 **Детальный анализ** - Включены скрипты анализа производительности
- 🧩 **Расширяемость** - Легко адаптируется для различных типов бенчмарков

## 🛠️ Предварительные требования

- Python 3.13.5 или выше
- [Ollama](https://ollama.com/) установлен и запущен

## 📦 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/laurentvv/bench-ai-ollama-lmstudio.git
   cd bench-ai-ollama-lmstudio
   ```

2. Создайте виртуальную среду и установите зависимости:
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🚀 Запуск бенчмарка

1. Убедитесь, что Ollama запущен.

2. Загрузите модель, которую хотите протестировать:
   ```bash
   ollama pull qwen3:14b
   ```

3. Запустите бенчмарк с выбранным набором данных:
   ```bash
   # Для HumanEval
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-openai-openai-humaneval.json
   ```

## 📊 Отслеживание с Weave

Bench AI интегрирован с [Weave](https://wandb.ai/site/weave), мощным инструментом для отслеживания и визуализации ваших экспериментов.

## 🧩 Поддерживаемые наборы данных

Этот репозиторий содержит **3 файла наборов данных** с **30 вопросами в каждом**:

- **`sql-console-for-openai-openai-humaneval.json`** - HumanEval (30 вопросов)
- **`sql-console-for-cruxeval-org-cruxeval.json`** - CruxEval (30 вопросов)
- **`sql-console-for-google-code-x-glue-ct-code-to-text.json`** - Code-X-GLUE (30 вопросов)

## 💯 Продвинутая оценка

Bench AI использует продвинутый подход к оценке, который объединяет несколько методов для обнаружения правильных ответов:

1. **Базовая нормализация**: Удаляет теги и нормализует пробелы
2. **Продвинутая нормализация**: Интеллектуально обрабатывает отступы и переносы строк
3. **Экстремальная нормализация**: Удаляет все пробелы и переносы строк
4. **Сравнение AST**: Анализирует синтаксическую структуру кода
5. **Оценка ИИ**: Использует языковую модель для обнаружения функциональной эквивалентности

## 🤝 Вклад

Вклады приветствуются! Не стесняйтесь открывать issue или отправлять pull request.

## 📄 Лицензия

Этот проект лицензирован под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.