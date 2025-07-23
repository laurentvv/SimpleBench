# System Patterns

## Architecture
SimpleBench utilise une architecture simple composée de plusieurs composants clés :

1. **Chargeur de Dataset** : Charge directement les datasets depuis leurs formats originaux
2. **Détecteur de Type** : Identifie automatiquement le type de dataset
3. **Interface Modèle** : Communique avec Ollama pour obtenir les réponses du modèle
4. **Évaluateur Multi-Méthodes** : Compare les réponses du modèle avec les réponses attendues en utilisant plusieurs approches
5. **Rapporteur** : Génère des rapports détaillés sur les performances du modèle

## Data Flow
```
Dataset Source → Détecteur de Type → Chargeur de Dataset → Questions → 
Interface Modèle → Réponses → Évaluateur → Scores → Rapporteur → Rapport de Performance
```

## Key Components

### Modèles (weave_utils/models.py)
- `LiteLLMModel` : Wrapper pour les modèles Ollama via LiteLLM
- `MajorityVoteModel` : Agrège plusieurs réponses pour améliorer la précision

### Chargeurs de Dataset (run_benchmark_new.py)
- `load_humaneval_dataset` : Charge les datasets HumanEval
- `load_cruxeval_dataset` : Charge les datasets CruxEval
- `load_code_x_glue_dataset` : Charge les datasets Code-X-GLUE
- `load_dataset_from_source` : Fonction générique qui utilise le détecteur de type

### Évaluation (run_benchmark_final.py)
- `normalize_code_basic` : Normalisation basique du code (suppression des balises, normalisation des espaces)
- `normalize_code_advanced` : Normalisation avancée du code (gestion intelligente de l'indentation)
- `normalize_code_extreme` : Normalisation extrême du code (suppression de tous les espaces et sauts de ligne)
- `compare_ast_structures` : Comparaison de la structure syntaxique du code
- `evaluate_code_final` : Fonction d'évaluation complète qui combine toutes les méthodes
- `run_benchmark` : Fonction principale qui orchestre le processus d'évaluation

## Design Decisions
1. **Script Unique** : Toutes les fonctionnalités sont intégrées dans un seul script pour simplifier l'utilisation
2. **Détection Automatique** : Le type de dataset est détecté automatiquement pour réduire la configuration manuelle
3. **Prompts Intégrés** : Les prompts système sont définis dans le code pour éliminer les dépendances externes
4. **Évaluation Multi-Méthodes** : Combinaison de plusieurs approches d'évaluation pour maximiser la détection des réponses correctes
5. **Support Exclusif d'Ollama** : Pour simplifier l'intégration et se concentrer sur un écosystème spécifique
6. **Approche en Cascade** : Les méthodes d'évaluation sont appliquées dans l'ordre, de la plus simple à la plus complexe
7. **Évaluation par IA** : Utilisation d'un modèle de langage pour détecter les équivalences fonctionnelles
8. **Analyse AST** : Utilisation de l'arbre syntaxique abstrait pour comparer la structure du code