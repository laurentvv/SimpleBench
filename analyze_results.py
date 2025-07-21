import json
import sys
import os

def analyze_results(results_file):
    """
    Analyse les résultats d'un benchmark et affiche des statistiques sur les limites du modèle.
    
    Args:
        results_file: Chemin vers le fichier JSON ou JSONL contenant les résultats du benchmark
    """
    if not os.path.exists(results_file):
        print(f"Le fichier {results_file} n'existe pas.")
        return
    
    # Déterminer si c'est un fichier JSON ou JSONL
    is_jsonl = results_file.endswith('.jsonl')
    
    try:
        if is_jsonl:
            # Pour JSONL, lire ligne par ligne
            results = {'eval_table': []}
            with open(results_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        line_data = json.loads(line.strip())
                        if 'output' in line_data and 'scores' in line_data['output']:
                            # Créer un format compatible avec notre analyse
                            entry = {
                                'dataset_id': line_data['inputs']['example'].get('question_id', 'Unknown'),
                                'evaluate_as_python_objects': line_data['output']['scores'].get('evaluate_as_python_objects', {})
                            }
                            results['eval_table'].append(entry)
                    except json.JSONDecodeError:
                        continue
        else:
            # Pour JSON standard
            with open(results_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {results_file}: {e}")
        return
    
    # Compteurs
    total = 0
    correct = 0
    incorrect = 0
    limit_reached = 0
    
    # Parcourir les résultats
    for item in results.get('eval_table', []):
        total += 1
        
        # Vérifier le résultat de l'évaluation
        if 'evaluate_as_python_objects' in item:
            eval_result = item['evaluate_as_python_objects']
            
            if eval_result.get('exact_match', False):
                correct += 1
            elif eval_result.get('reason') == 'model_limit_reached':
                limit_reached += 1
            else:
                incorrect += 1
    
    # Calculer les pourcentages
    correct_pct = (correct / total) * 100 if total > 0 else 0
    incorrect_pct = (incorrect / total) * 100 if total > 0 else 0
    limit_pct = (limit_reached / total) * 100 if total > 0 else 0
    
    # Afficher les résultats
    print(f"\n=== Analyse des résultats du benchmark ===")
    print(f"Total des questions: {total}")
    print(f"Réponses correctes: {correct} ({correct_pct:.1f}%)")
    print(f"Réponses incorrectes: {incorrect} ({incorrect_pct:.1f}%)")
    print(f"Limites du modèle atteintes: {limit_reached} ({limit_pct:.1f}%)")
    
    # Afficher les questions où la limite a été atteinte
    if limit_reached > 0:
        print("\nQuestions où la limite du modèle a été atteinte:")
        for i, item in enumerate(results.get('eval_table', [])):
            if 'evaluate_as_python_objects' in item and item['evaluate_as_python_objects'].get('reason') == 'model_limit_reached':
                question_id = item.get('dataset_id', f"Question {i}")
                print(f"- {question_id}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_results.py <results_file.json>")
        sys.exit(1)
    
    analyze_results(sys.argv[1])