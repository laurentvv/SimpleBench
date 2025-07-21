# Project Brief: SimpleBench

## Overview
SimpleBench est un outil de benchmark simple pour évaluer les modèles de langage, spécifiquement adapté pour tester les modèles utilisant Ollama. Le projet permet d'exécuter des tests standardisés sur différents modèles et de comparer leurs performances.

## Core Requirements
1. Exécuter des benchmarks sur des modèles de langage via Ollama
2. Charger des datasets de questions/réponses au format JSON
3. Évaluer les réponses des modèles par rapport aux réponses attendues
4. Générer des rapports de performance

## Technical Constraints
- Python 3.13.5 ou supérieur
- Ollama doit être installé et en cours d'exécution
- Les modèles doivent être téléchargés via Ollama avant les tests

## Success Criteria
- Capacité à exécuter des benchmarks sur différents modèles Ollama
- Évaluation correcte des réponses, indépendamment des différences de formatage
- Rapports clairs sur les performances des modèles