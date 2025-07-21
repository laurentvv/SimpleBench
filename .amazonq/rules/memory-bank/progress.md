# Progress

## Fonctionnalités Implémentées
- ✅ Chargement de datasets au format JSON
- ✅ Intégration avec Ollama via LiteLLM
- ✅ Évaluation des réponses des modèles
- ✅ Support de différents modèles Ollama
- ✅ Conversion de datasets entre différents formats
- ✅ Évaluation robuste qui tolère les différences de formatage
- ✅ Détection des limites du modèle (max tokens)
- ✅ Scripts d'analyse des résultats (statistiques et vérification)
- ✅ Détection automatique des nouveaux modèles Ollama
- ✅ Support de différents formats de réponse (think/markdown/texte)

## Problèmes Résolus
- ✅ Problème de comparaison des réponses avec différents formats de guillemets
- ✅ Extraction correcte des réponses du modèle (séparation du raisonnement et de la réponse)
- ✅ Simplification de la logique d'évaluation pour plus de robustesse
- ✅ Traitement spécial pour les questions problématiques (liste de tuples, caractères répétés)
- ✅ Gestion des différents formats de réponse selon le modèle utilisé
- ✅ Identification des cas où le modèle atteint sa limite de tokens

## En Cours
- 🔄 Tests avec différents modèles Ollama
- 🔄 Optimisation des performances du benchmark

## À Faire
- ⏳ Support de datasets personnalisés plus complexes
- ⏳ Interface utilisateur pour visualiser les résultats
- ⏳ Comparaison automatique entre différents modèles
- ⏳ Documentation plus détaillée
- ⏳ Parallélisation des évaluations pour améliorer les performances

## Décisions Techniques
- Utilisation de Weave pour le suivi des résultats
- Approche multi-méthodes pour l'évaluation des réponses (normalisation, extraction, comptage)
- Séparation claire entre le chargement des données, l'exécution du modèle et l'évaluation
- Scripts d'analyse séparés pour faciliter l'interprétation des résultats
- Détection automatique des modèles pour simplifier l'utilisation