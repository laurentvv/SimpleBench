# System Patterns

## Architecture
SimpleBench utilise une architecture simple composée de plusieurs composants clés :

1. **Chargeur de Dataset** : Charge les questions et réponses attendues depuis un fichier JSON
2. **Interface Modèle** : Communique avec Ollama pour obtenir les réponses du modèle
3. **Évaluateur** : Compare les réponses du modèle avec les réponses attendues
4. **Rapporteur** : Génère des rapports sur les performances du modèle

## Data Flow
```
Dataset JSON → Chargeur de Dataset → Questions → Interface Modèle → Réponses → 
Évaluateur → Scores → Rapporteur → Rapport de Performance
```

## Key Components

### Modèles (weave_utils/models.py)
- `LiteLLMModel` : Wrapper pour les modèles Ollama via LiteLLM
- `MajorityVoteModel` : Agrège plusieurs réponses pour améliorer la précision

### Évaluation (run_benchmark_new.py)
- `evaluate_as_python_objects` : Fonction d'évaluation qui compare les réponses
- `load_dataset` : Charge le dataset depuis un fichier JSON
- `run_benchmark` : Fonction principale qui orchestre le processus d'évaluation

### Conversion de Dataset (convert_dataset.py)
- Convertit les datasets d'un format à un autre pour la compatibilité

## Design Decisions
1. **Utilisation de Weave** : Pour le suivi et la visualisation des résultats
2. **Normalisation des réponses** : Suppression des guillemets et espaces pour une comparaison robuste
3. **Support exclusif d'Ollama** : Pour simplifier l'intégration et se concentrer sur un écosystème spécifique