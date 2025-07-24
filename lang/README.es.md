# Bench AI with Ollama/LMStudio

<div align="center">

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Bench AI Logo](https://img.shields.io/badge/Bench%20AI-LLM%20Benchmark%20Tool-blue)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

Bench AI es una herramienta ligera y eficiente para evaluar el rendimiento de modelos de lenguaje (LLMs) ejecutados a través de [Ollama](https://ollama.com/) y LMStudio. Permite a investigadores y desarrolladores comparar objetivamente diferentes modelos en tareas estandarizadas de programación y razonamiento.

## 🎯 Resultados Recientes

- **Precisión de evaluación**: 63% de respuestas correctas detectadas en HumanEval
- **Métodos de evaluación**: 5 enfoques complementarios (normalización, AST, IA)
- **Reproducibilidad**: Resultados consistentes entre ejecuciones

## ✨ Características

- 🚀 **Fácil de usar** - Interfaz de línea de comandos intuitiva
- 🔄 **Soporte multi-dataset** - Compatible con HumanEval, CruxEval y Code-X-GLUE
- 📊 **Evaluación avanzada** - Tolera diferencias de formato, indentación y equivalencia funcional
- 📈 **Análisis detallado** - Scripts de análisis de rendimiento incluidos
- 🧩 **Extensible** - Fácil de adaptar para diferentes tipos de benchmarks

## 🛠️ Prerrequisitos

- Python 3.13.5 o superior
- [Ollama](https://ollama.com/) instalado y ejecutándose

## 📦 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/laurentvv/bench-ai-ollama-lmstudio.git
   cd bench-ai-ollama-lmstudio
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🚀 Ejecutar el benchmark

1. Asegúrate de que Ollama esté ejecutándose.

2. Descarga el modelo que quieres probar:
   ```bash
   ollama pull qwen3:14b
   ```

3. Ejecuta el benchmark con un dataset de tu elección:
   ```bash
   # Para HumanEval
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-openai-openai-humaneval.json
   
   # Para CruxEval
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-cruxeval-org-cruxeval.json
   
   # Para Code-X-GLUE
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-google-code-x-glue-ct-code-to-text.json
   ```

## 📊 Seguimiento con Weave

Bench AI está integrado con [Weave](https://wandb.ai/site/weave), una herramienta poderosa para rastrear y visualizar tus experimentos.

### Configuración de Weave

Para habilitar el seguimiento con Weave, usa las opciones `--entity` y `--project` al ejecutar el benchmark:

```bash
python run_benchmark_production.py \
  --model_name=qwen3:14b \
  --dataset_source=sql-console-for-openai-openai-humaneval.json \
  --entity="tu-entidad-weave" \
  --project="nombre-proyecto"
```

## 🧩 Datasets Soportados

Este repositorio contiene **3 archivos de datasets** con **30 preguntas cada uno**:

- **`sql-console-for-openai-openai-humaneval.json`** - HumanEval (30 preguntas)
- **`sql-console-for-cruxeval-org-cruxeval.json`** - CruxEval (30 preguntas)
- **`sql-console-for-google-code-x-glue-ct-code-to-text.json`** - Code-X-GLUE (30 preguntas)

## 💯 Evaluación Avanzada

Bench AI utiliza un enfoque de evaluación avanzado que combina múltiples métodos para detectar respuestas correctas:

1. **Normalización básica**: Elimina etiquetas y normaliza espacios
2. **Normalización avanzada**: Maneja inteligentemente la indentación y saltos de línea
3. **Normalización extrema**: Elimina todos los espacios y saltos de línea
4. **Comparación AST**: Analiza la estructura sintáctica del código
5. **Evaluación por IA**: Usa un modelo de lenguaje para detectar equivalencias funcionales

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! No dudes en abrir un issue o enviar un pull request.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para detalles.