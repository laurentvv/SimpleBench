# Simple Bench

https://simple-bench.com/

Ce dépôt a été modifié pour tester exclusivement les modèles utilisant Ollama.

## Instructions d'exécution

Assurez-vous d'abord qu'Ollama est installé et en cours d'exécution. Vous pouvez le télécharger sur [https://ollama.com/](https://ollama.com/).

Une fois Ollama en cours d'exécution, vous pouvez télécharger les modèles que vous souhaitez tester. Par exemple, pour télécharger le modèle `qwen3:14b-q4_K_M`, exécutez :

```
ollama pull qwen3:14b-q4_K_M
```

Ensuite, exécutez le benchmark :
```
python run_benchmark.py --model_name=qwen3:14b-q4_K_M --dataset_path=simple_bench_public.json
```

## Comment ajouter de nouveaux modèles

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

## Instructions de configuration

Clonez le dépôt github et placez-vous dedans.

Installez les dépendances:

La meilleure façon d'installer les dépendances est d'utiliser `uv`. Si vous ne l'avez pas installé dans votre environnement, vous pouvez l'installer avec `pip install uv`.

`uv` créera automatiquement un environnement virtuel et installera les dépendances à partir de `pyproject.toml`.

```
uv pip sync
```
