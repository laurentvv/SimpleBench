# SimpleBench

<div align="center">

![SimpleBench Logo](https://img.shields.io/badge/SimpleBench-Benchmark%20for%20LLMs-blue)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

SimpleBench est un outil léger et efficace pour évaluer les performances des modèles de langage (LLMs) exécutés via [Ollama](https://ollama.com/). Il permet aux chercheurs et développeurs de comparer objectivement différents modèles sur des tâches standardisées de programmation et de raisonnement.

## ✨ Caractéristiques

- 🚀 **Simple d'utilisation** - Interface en ligne de commande intuitive
- 🔄 **Détection automatique des modèles** - Pas besoin de configuration manuelle
- 📊 **Évaluation robuste** - Tolère les différences de formatage dans les réponses
- 📈 **Analyse détaillée** - Scripts d'analyse des performances inclus
- 🧩 **Extensible** - Facile à adapter pour différents types de benchmarks

## 🛠️ Prérequis

- Python 3.13.5 ou supérieur
- [Ollama](https://ollama.com/) installé et en cours d'exécution

## 📦 Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/simple-bench/simple-bench.git
   cd simple-bench
   ```

2. Créez un environnement virtuel et installez les dépendances :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🚀 Exécution du benchmark

1. Assurez-vous qu'Ollama est en cours d'exécution.

2. Téléchargez le modèle que vous souhaitez tester :
   ```bash
   ollama pull qwen3:14b
   ```

3. Exécutez le benchmark :
   ```bash
   python run_benchmark_new.py --model_name=qwen3:14b --dataset_path=converted_code_bench.json
   ```

### Options disponibles

| Option | Description | Valeur par défaut |
|--------|-------------|-------------------|
| `--model_name` | Nom du modèle Ollama à tester | qwen3:14b |
| `--dataset_path` | Chemin vers le fichier JSON du dataset | ./converted_code_bench.json |
| `--num_responses` | Nombre de réponses pour le vote majoritaire | 1 |
| `--temp` | Température pour le modèle | 0.7 |
| `--max_tokens` | Nombre maximum de tokens à générer | 2048 |
| `--top_p` | Valeur top_p pour le modèle | 0.95 |
| `--max_retries` | Nombre maximum de tentatives en cas d'erreur | 3 |

## 📊 Analyse des résultats

Après avoir exécuté le benchmark, vous pouvez analyser les résultats avec les scripts fournis :

### Statistiques générales

```bash
python analyze_results.py weave_export_simple_bench_[date].jsonl
```

Ce script affiche :
- Le nombre total de questions
- Le nombre et pourcentage de réponses correctes
- Le nombre et pourcentage de réponses incorrectes
- Le nombre et pourcentage de cas où la limite du modèle a été atteinte

### Vérification détaillée des réponses

```bash
python verify_responses.py weave_export_simple_bench_[date].jsonl
```

Ce script affiche une comparaison détaillée entre les réponses du modèle et les réponses attendues pour chaque question.

## 🧩 Ajout de nouveaux modèles

Le script détecte automatiquement les nouveaux modèles Ollama, il n'est donc plus nécessaire de modifier manuellement le code. Il suffit de spécifier le nom du modèle dans la commande :

```bash
python run_benchmark_new.py --model_name=nom-du-modele --dataset_path=converted_code_bench.json
```

Par exemple, pour tester le modèle `llama3:8b` :

```bash
ollama pull llama3:8b
python run_benchmark_new.py --model_name=llama3:8b --dataset_path=converted_code_bench.json
```

Le modèle sera automatiquement préfixé avec "ollama/" et configuré lors de l'exécution.

## 📝 Format du dataset

### Source des questions

Les questions utilisées dans ce benchmark proviennent du dataset [CruxEval](https://huggingface.co/datasets/cruxeval-org/cruxeval), un ensemble de problèmes de programmation conçu pour évaluer les capacités de raisonnement des modèles de langage.

### Structure du dataset

Les datasets doivent être au format JSON avec la structure suivante :

```json
{
  "eval_data": [
    {
      "question_id": 0,
      "prompt": "Question...",
      "answer": "Réponse attendue"
    },
    ...
  ]
}
```

### Conversion de datasets

Le script `convert_dataset.py` permet de convertir les données du format JSONL original de CruxEval vers le format JSON utilisé par SimpleBench :

```bash
python convert_dataset.py
```

Ce script :
- Lit le fichier JSONL source (`test.jsonl_copy.txt`)
- Extrait les questions, entrées et sorties attendues
- Formate les prompts en français
- Génère un fichier JSON compatible (`converted_code_bench.json`)

### Datasets additionnels à tester

SimpleBench peut être adapté pour fonctionner avec d'autres datasets de référence pour l'évaluation des modèles de langage sur des tâches de programmation :

- [HumanEval](https://huggingface.co/datasets/openai/openai_humaneval) - Un benchmark d'OpenAI pour évaluer les capacités de génération de code
- [CodeXGLUE](https://huggingface.co/datasets/google/code_x_glue_ct_code_to_text) - Un benchmark de Google pour diverses tâches liées au code

Pour utiliser ces datasets, il faudra adapter le script de conversion pour transformer leurs formats spécifiques au format JSON attendu par SimpleBench.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.