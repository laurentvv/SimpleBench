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
- **run_benchmark.py** / **run_benchmark_new.py** : Scripts principaux pour exécuter les benchmarks
- **convert_dataset.py** : Utilitaire pour convertir les formats de dataset
- **weave_utils/** : Modules utilitaires pour l'intégration avec Weave
  - **models.py** : Définitions des modèles
  - **scorers.py** : Fonctions d'évaluation

## Format de Données
- **Dataset JSON** : Format utilisé pour les questions et réponses
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

## Configuration
- **Prompt système** : Défini dans un fichier texte séparé
- **Paramètres du modèle** : Température, top_p, max_tokens, etc.