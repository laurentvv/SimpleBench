# Tech Context

## Technologies Utilisées

### Langages
- **Python 3.13.5+** : Langage principal du projet

### Bibliothèques Principales
- **Weave** : Pour le suivi et la visualisation des résultats d'évaluation
- **LiteLLM** : Pour l'interface avec différents modèles de langage
- **Fire** : Pour l'interface en ligne de commande
- **asyncio** : Pour la gestion des opérations asynchrones

### Outils Externes
- **Ollama** : Plateforme pour exécuter des modèles de langage localement
- **Weights & Biases (W&B)** : Pour le stockage et la visualisation des résultats

## Environnement de Développement
- **uv** : Gestionnaire de paquets Python recommandé
- **Environnement virtuel Python** : Créé automatiquement par uv

## Structure des Fichiers
- **run_benchmark_new.py** : Script principal pour exécuter les benchmarks
- **analyze_results.py** : Script pour analyser les statistiques des résultats
- **verify_responses.py** : Script pour vérifier les réponses individuelles
- **weave_utils/** : Modules utilitaires pour l'intégration avec Weave
  - **models.py** : Définitions des modèles
  - **scorers.py** : Fonctions d'évaluation

## Datasets Supportés
- **HumanEval** : Benchmark d'OpenAI pour l'évaluation de la génération de code
- **CruxEval** : Benchmark pour évaluer les capacités de raisonnement
- **Code-X-GLUE** : Benchmark de Google pour les tâches liées au code

## Fonctionnalités Clés
- **Détection automatique des datasets** : Identification du type de dataset basée sur le nom du fichier ou son contenu
- **Prompts système intégrés** : Prompts spécifiques pour chaque type de dataset
- **Évaluation adaptative** : Méthodes d'évaluation adaptées selon le type de dataset
- **Normalisation des réponses** : Plusieurs méthodes pour comparer les réponses malgré les différences de formatage

## Configuration
- **Paramètres du modèle** : Température, top_p, max_tokens, etc.
- **Options de benchmark** : Type de dataset, nombre de réponses pour le vote majoritaire, etc.