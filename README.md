# Simple Bench

Ce projet est un benchmark simple pour évaluer les modèles de langage. Il a été modifié pour tester exclusivement les modèles utilisant Ollama.

## Table des matières

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Exécution du benchmark](#exécution-du-benchmark)
- [Ajout de nouveaux modèles](#ajout-de-nouveaux-modèles)

## Prérequis

- Python 3.13.5 ou supérieur
- [Ollama](https://ollama.com/)

## Installation

1.  Clonez le dépôt :
    ```bash
    git clone https://github.com/simple-bench/simple-bench.git
    cd simple-bench
    ```

2.  Installez les dépendances à l'aide de `uv` :
    ```bash
    uv pip sync --python 3.13.5
    ```
    Si vous n'avez pas `uv`, vous pouvez l'installer avec `pip install uv`. `uv` créera automatiquement un environnement virtuel et installera les dépendances à partir de `pyproject.toml`.

## Exécution du benchmark

1.  Assurez-vous qu'Ollama est en cours d'exécution.

2.  Téléchargez le modèle que vous souhaitez tester. Par exemple, pour télécharger le modèle `qwen3:14b-q4_K_M`, exécutez :
    ```bash
    ollama pull qwen3:14b-q4_K_M
    ```

3.  Exécutez le benchmark :
    ```bash
    python run_benchmark.py --model_name=qwen3:14b-q4_K_M --dataset_path=simple_bench_public.json
    ```

## Ajout de nouveaux modèles

Pour ajouter un nouveau modèle, vous devez le modifier le dictionnaire `MODEL_MAP` dans le fichier `weave_utils/models.py`.

Par exemple, pour ajouter le modèle `my-new-model`, vous devez modifier le dictionnaire comme suit :

```python
MODEL_MAP = {
    "llama3": "llama3",
    "llama2": "llama2",
    "codellama": "codellama",
    "mistral": "mistral",
    "mixtral": "mixtral",
    "llava": "llava",
    "gemma": "gemma",
    "phi3": "phi3",
    "qwen2": "qwen2",
    "qwen3:14b-q4_K_M": "qwen3:14b-q4_K_M",
    "command-r": "command-r",
    "command-r-plus": "command-r-plus",
    "my-new-model": "my-new-model",
}
```
