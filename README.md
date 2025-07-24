# Bench AI with Ollama/LMStudio

<div align="center">

![Bench AI Logo](https://img.shields.io/badge/Bench%20AI-LLM%20Benchmark%20Tool-blue)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

Bench AI est un outil léger et efficace pour évaluer les performances des modèles de langage (LLMs) exécutés via [Ollama](https://ollama.com/) et LMStudio. Il permet aux chercheurs et développeurs de comparer objectivement différents modèles sur des tâches standardisées de programmation et de raisonnement.

## 🎯 Résultats Récents

- **Précision d'évaluation** : 63% de réponses correctes détectées sur HumanEval
- **Méthodes d'évaluation** : 5 approches complémentaires (normalisation, AST, IA)
- **Reproductibilité** : Résultats cohérents entre les exécutions

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
   git clone https://github.com/laurentvv/bench-ai-ollama-lmstudio.git
   cd bench-ai-ollama-lmstudio
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
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-openai-openai-humaneval.json
   
   # Pour CruxEval
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-cruxeval-org-cruxeval.json
   
   # Pour Code-X-GLUE
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-google-code-x-glue-ct-code-to-text.json
   ```

## ιχ Suivi avec Weave

Bench AI est intégré avec [Weave](https://wandb.ai/site/weave), un outil puissant pour le suivi et la visualisation de vos expériences.

### Configuration de Weave

1. **Créez un compte Weave** : Rendez-vous sur le [site de Weave](https://wandb.ai/site/weave) et créez un compte gratuit.

2. **Connectez-vous à Weave** : Une fois votre compte créé, vous pouvez vous connecter via le CLI (non nécessaire pour ce projet, géré par l'API).

### Utilisation de Weave avec SimpleBench

Pour activer le suivi avec Weave, utilisez les options `--entity` et `--project` lors de l'exécution du benchmark :

```bash
python run_benchmark_production.py \
  --model_name=qwen3:14b \
  --dataset_source=sql-console-for-openai-openai-humaneval.json \
  --entity="votre-entite-weave" \
  --project="nom-du-projet"
```

- `--entity` : Votre nom d'utilisateur ou d'organisation Weave.
- `--project` : Le nom du projet sous lequel vous souhaitez enregistrer l'expérience.

Les résultats de l'évaluation, y compris les scores détaillés et les prédictions du modèle, seront automatiquement envoyés à votre projet Weave, vous permettant de :

- Comparer les performances de différents modèles
- Analyser les erreurs de prédiction
- Partager vos résultats avec votre équipe

### Options disponibles

| Option | Description | Valeur par défaut |
|--------|-------------|-------------------|
| `--model_name` | Nom du modèle Ollama à tester | qwen3:14b |
| `--dataset_source` | Chemin vers le fichier source du dataset | ./sql-console-for-openai-openai-humaneval.json |
| `--dataset_type` | Type de dataset (humaneval, cruxeval, code_x_glue) | auto-détecté |
| `--num_responses` | Nombre de réponses pour le vote majoritaire | 1 |
| `--temp` | Température pour le modèle | 0.1 |
| `--max_tokens` | Nombre maximum de tokens à générer | 2048 |
| `--top_p` | Valeur top_p pour le modèle | 0.95 |
| `--max_retries` | Nombre maximum de tentatives en cas d'erreur | 3 |
| `--custom_system_prompt` | Prompt système personnalisé | prompt par défaut selon le dataset |

## 📊 Analyse des résultats

Le script `run_benchmark_production.py` affiche automatiquement les résultats détaillés de l'évaluation, notamment :

- Le nombre total de questions évaluées
- Le nombre et pourcentage de réponses correctes
- Le temps d'exécution total
- La répartition des réponses correctes par méthode d'évaluation :
  - **Normalisation basique** : Correspondance exacte après nettoyage
  - **Normalisation avancée** : Gestion intelligente de l'indentation
  - **Normalisation extrême** : Suppression des espaces et sauts de ligne
  - **Comparaison AST** : Analyse de la structure syntaxique
  - **Équivalence IA** : Détection d'équivalence fonctionnelle

Ces statistiques détaillées vous permettent de comprendre précisément les performances du modèle et les types de réponses qu'il génère.

## 🧩 Datasets supportés

Bench AI supporte nativement plusieurs datasets populaires pour l'évaluation des modèles de langage :

### 📁 Datasets inclus dans ce dépôt

Ce dépôt contient **3 fichiers de datasets** avec **30 questions chacun** :

- **`sql-console-for-openai-openai-humaneval.json`** - HumanEval (30 questions)
- **`sql-console-for-cruxeval-org-cruxeval.json`** - CruxEval (30 questions)  
- **`sql-console-for-google-code-x-glue-ct-code-to-text.json`** - Code-X-GLUE (30 questions)

> 💡 **Pour plus de questions**, consultez les datasets complets sur Hugging Face (liens ci-dessous)

### HumanEval

[HumanEval](https://huggingface.co/datasets/openai/openai_humaneval) est un benchmark d'OpenAI pour évaluer les capacités de génération de code. Il contient des problèmes de programmation Python avec des solutions et des tests.

### CruxEval

[CruxEval](https://huggingface.co/datasets/cruxeval-org/cruxeval) est un ensemble de problèmes de programmation conçu pour évaluer les capacités de raisonnement des modèles de langage.

### Code-X-GLUE

[CodeXGLUE](https://huggingface.co/datasets/google/code_x_glue_ct_code_to_text) est un benchmark de Google pour diverses tâches liées au code, notamment la génération de descriptions à partir de code source.

## 🔧 Détection automatique des datasets

Bench AI détecte automatiquement le type de dataset en fonction du nom du fichier ou de son contenu. Vous pouvez également spécifier explicitement le type avec l'option `--dataset_type`.

## 💯 Évaluation avancée

Bench AI utilise une approche d'évaluation avancée qui combine plusieurs méthodes pour détecter les réponses correctes :

1. **Normalisation basique** : Supprime les balises et normalise les espaces
2. **Normalisation avancée** : Gère intelligemment l'indentation et les sauts de ligne
3. **Normalisation extrême** : Supprime tous les espaces et sauts de ligne pour détecter les réponses qui diffèrent uniquement par le formatage
4. **Comparaison AST** : Analyse la structure syntaxique du code pour détecter les équivalences structurelles
5. **Évaluation par IA** : Utilise un modèle de langage pour détecter les équivalences fonctionnelles

Cette approche permet de détecter beaucoup plus précisément les réponses correctes, même lorsqu'elles diffèrent de la solution attendue en termes de style, de noms de variables ou d'approche algorithmique.

## 🚀 Prochaines Fonctionnalités

- Support de LMStudio pour les modèles locaux
- Dataset MBPP (Mostly Basic Python Problems)
- Interface web pour visualiser les résultats
- Comparaison automatique entre modèles

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.