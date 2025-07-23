# SimpleBench

<div align="center">

![SimpleBench Logo](https://img.shields.io/badge/SimpleBench-Benchmark%20for%20LLMs-blue)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

SimpleBench est un outil léger et efficace pour évaluer les performances des modèles de langage (LLMs) exécutés via [Ollama](https://ollama.com/). Il permet aux chercheurs et développeurs de comparer objectivement différents modèles sur des tâches standardisées de programmation et de raisonnement.

## ✨ Caractéristiques

- 🚀 **Simple d'utilisation** - Interface en ligne de commande intuitive
- 🔄 **Support multi-datasets** - Compatible avec HumanEval, CruxEval et Code-X-GLUE
- 📊 **Évaluation avancée** - Tolère les différences de formatage, d'indentation et d'équivalence fonctionnelle
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

3. Exécutez le benchmark avec un dataset au choix :
   ```bash
   # Pour HumanEval
   python run_benchmark_final.py --model_name=qwen3:14b --dataset_source=sql-console-for-openai-openai-humaneval.json
   
   # Pour CruxEval
   python run_benchmark_final.py --model_name=qwen3:14b --dataset_source=sql-console-for-cruxeval-org-cruxeval.json
   
   # Pour Code-X-GLUE
   python run_benchmark_final.py --model_name=qwen3:14b --dataset_source=sql-console-for-google-code-x-glue-ct-code-to-text.json
   ```

### Options disponibles

| Option | Description | Valeur par défaut |
|--------|-------------|-------------------|
| `--model_name` | Nom du modèle Ollama à tester | qwen3:14b |
| `--dataset_source` | Chemin vers le fichier source du dataset | ./sql-console-for-openai-openai-humaneval.json |
| `--dataset_type` | Type de dataset (humaneval, cruxeval, code_x_glue) | auto-détecté |
| `--num_responses` | Nombre de réponses pour le vote majoritaire | 1 |
| `--temp` | Température pour le modèle | 0.7 |
| `--max_tokens` | Nombre maximum de tokens à générer | 2048 |
| `--top_p` | Valeur top_p pour le modèle | 0.95 |
| `--max_retries` | Nombre maximum de tentatives en cas d'erreur | 3 |
| `--custom_system_prompt` | Prompt système personnalisé | prompt par défaut selon le dataset |

## 📊 Analyse des résultats

Le script `run_benchmark_final.py` affiche automatiquement les résultats détaillés de l'évaluation, notamment :

- Le nombre total de questions évaluées
- Le nombre et pourcentage de réponses correctes
- La répartition des réponses correctes par méthode d'évaluation :
  - Normalisation basique (correspondance exacte après nettoyage)
  - Normalisation avancée (gestion de l'indentation)
  - Normalisation extrême (suppression des espaces et sauts de ligne)
  - Comparaison AST (analyse de la structure syntaxique)
  - Équivalence IA (détection d'équivalence fonctionnelle)

Ces statistiques détaillées vous permettent de comprendre précisément les performances du modèle et les types de réponses qu'il génère.

## 🧩 Datasets supportés

SimpleBench supporte nativement plusieurs datasets populaires pour l'évaluation des modèles de langage :

### HumanEval

[HumanEval](https://huggingface.co/datasets/openai/openai_humaneval) est un benchmark d'OpenAI pour évaluer les capacités de génération de code. Il contient des problèmes de programmation Python avec des solutions et des tests.

### CruxEval

[CruxEval](https://huggingface.co/datasets/cruxeval-org/cruxeval) est un ensemble de problèmes de programmation conçu pour évaluer les capacités de raisonnement des modèles de langage.

### Code-X-GLUE

[CodeXGLUE](https://huggingface.co/datasets/google/code_x_glue_ct_code_to_text) est un benchmark de Google pour diverses tâches liées au code, notamment la génération de descriptions à partir de code source.

## 🔧 Détection automatique des datasets

SimpleBench détecte automatiquement le type de dataset en fonction du nom du fichier ou de son contenu. Vous pouvez également spécifier explicitement le type avec l'option `--dataset_type`.

## 💯 Évaluation avancée

SimpleBench utilise une approche d'évaluation avancée qui combine plusieurs méthodes pour détecter les réponses correctes :

1. **Normalisation basique** : Supprime les balises et normalise les espaces
2. **Normalisation avancée** : Gère intelligemment l'indentation et les sauts de ligne
3. **Normalisation extrême** : Supprime tous les espaces et sauts de ligne pour détecter les réponses qui diffèrent uniquement par le formatage
4. **Comparaison AST** : Analyse la structure syntaxique du code pour détecter les équivalences structurelles
5. **Évaluation par IA** : Utilise un modèle de langage pour détecter les équivalences fonctionnelles

Cette approche permet de détecter beaucoup plus précisément les réponses correctes, même lorsqu'elles diffèrent de la solution attendue en termes de style, de noms de variables ou d'approche algorithmique.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.