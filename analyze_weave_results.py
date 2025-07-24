#!/usr/bin/env python3
"""
Script d'analyse des résultats Weave pour SimpleBench
Analyse les performances, latences et méthodes d'évaluation
"""

import json
import statistics
from datetime import datetime
from collections import Counter, defaultdict

def load_weave_export(file_path):
    """Charge les données d'export Weave"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_performance(data):
    """Analyse les performances globales"""
    total_questions = len(data)
    correct_answers = sum(1 for item in data if item['output']['scores']['score_function']['exact_match'])
    accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    return {
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'accuracy_percentage': accuracy
    }

def analyze_latency(data):
    """Analyse les temps de latence"""
    latencies = [item['output']['model_latency'] for item in data if 'model_latency' in item['output']]
    
    if not latencies:
        return {}
    
    return {
        'min_latency': min(latencies),
        'max_latency': max(latencies),
        'mean_latency': statistics.mean(latencies),
        'median_latency': statistics.median(latencies),
        'total_latency': sum(latencies)
    }

def analyze_evaluation_methods(data):
    """Analyse les méthodes d'évaluation utilisées"""
    methods = []
    for item in data:
        if 'scores' in item['output'] and 'score_function' in item['output']['scores']:
            reason = item['output']['scores']['score_function'].get('reason', 'unknown')
            methods.append(reason)
    
    return Counter(methods)

def analyze_question_difficulty(data):
    """Analyse la difficulté des questions basée sur la latence"""
    question_stats = []
    
    for item in data:
        question_id = item['inputs']['example']['question_id']
        latency = item['output'].get('model_latency', 0)
        is_correct = item['output']['scores']['score_function']['exact_match']
        
        question_stats.append({
            'question_id': question_id,
            'latency': latency,
            'is_correct': is_correct
        })
    
    # Trier par latence pour identifier les questions difficiles
    question_stats.sort(key=lambda x: x['latency'], reverse=True)
    
    return question_stats

def analyze_temporal_patterns(data):
    """Analyse les patterns temporels"""
    timestamps = []
    for item in data:
        start_time = datetime.fromisoformat(item['started_at'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(item['ended_at'].replace('Z', '+00:00'))
        duration = (end_time - start_time).total_seconds()
        timestamps.append({
            'start': start_time,
            'end': end_time,
            'duration': duration
        })
    
    timestamps.sort(key=lambda x: x['start'])
    
    total_duration = (timestamps[-1]['end'] - timestamps[0]['start']).total_seconds()
    
    return {
        'total_execution_time': total_duration,
        'first_question_start': timestamps[0]['start'],
        'last_question_end': timestamps[-1]['end'],
        'average_question_duration': statistics.mean([t['duration'] for t in timestamps])
    }

def generate_report(file_path):
    """Génère un rapport complet d'analyse"""
    print("🔍 Analyse des résultats Weave SimpleBench")
    print("=" * 50)
    
    try:
        data = load_weave_export(file_path)
        print(f"✅ Fichier chargé: {len(data)} entrées trouvées")
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return
    
    # Analyse des performances
    print("\n📊 PERFORMANCES GLOBALES")
    print("-" * 30)
    perf = analyze_performance(data)
    print(f"Questions totales: {perf['total_questions']}")
    print(f"Réponses correctes: {perf['correct_answers']}")
    print(f"Précision: {perf['accuracy_percentage']:.1f}%")
    
    # Analyse des latences
    print("\n⏱️  ANALYSE DES LATENCES")
    print("-" * 30)
    latency = analyze_latency(data)
    if latency:
        print(f"Latence minimale: {latency['min_latency']:.2f}s")
        print(f"Latence maximale: {latency['max_latency']:.2f}s")
        print(f"Latence moyenne: {latency['mean_latency']:.2f}s")
        print(f"Latence médiane: {latency['median_latency']:.2f}s")
        print(f"Temps total modèle: {latency['total_latency']:.2f}s")
    
    # Analyse des méthodes d'évaluation
    print("\n🎯 MÉTHODES D'ÉVALUATION")
    print("-" * 30)
    methods = analyze_evaluation_methods(data)
    for method, count in methods.most_common():
        percentage = (count / len(data)) * 100
        print(f"{method}: {count} ({percentage:.1f}%)")
    
    # Questions les plus difficiles (par latence)
    print("\n🔥 QUESTIONS LES PLUS DIFFICILES")
    print("-" * 30)
    difficulty = analyze_question_difficulty(data)
    print("Top 5 par latence:")
    for i, q in enumerate(difficulty[:5], 1):
        status = "✅" if q['is_correct'] else "❌"
        print(f"{i}. Question {q['question_id']}: {q['latency']:.2f}s {status}")
    
    # Analyse temporelle
    print("\n⏰ ANALYSE TEMPORELLE")
    print("-" * 30)
    temporal = analyze_temporal_patterns(data)
    print(f"Durée totale d'exécution: {temporal['total_execution_time']:.2f}s")
    print(f"Durée moyenne par question: {temporal['average_question_duration']:.2f}s")
    print(f"Début: {temporal['first_question_start'].strftime('%H:%M:%S')}")
    print(f"Fin: {temporal['last_question_end'].strftime('%H:%M:%S')}")
    
    # Statistiques détaillées par question
    print("\n📋 DÉTAIL PAR QUESTION")
    print("-" * 30)
    for item in sorted(data, key=lambda x: x['inputs']['example']['question_id']):
        q_id = item['inputs']['example']['question_id']
        latency = item['output'].get('model_latency', 0)
        is_correct = item['output']['scores']['score_function']['exact_match']
        method = item['output']['scores']['score_function'].get('reason', 'unknown')
        status = "✅" if is_correct else "❌"
        print(f"Q{q_id:2d}: {latency:6.2f}s | {method:12s} | {status}")

def main():
    """Fonction principale"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python analyze_weave_results.py <fichier_export_weave.json>")
        print("Exemple: python analyze_weave_results.py weave_export_simple_bench_2025-07-24.json")
        sys.exit(1)
    
    file_path = sys.argv[1]
    generate_report(file_path)

if __name__ == "__main__":
    main()