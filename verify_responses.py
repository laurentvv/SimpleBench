import json
import sys
import os

def verify_responses(results_file):
    """
    Vérifie les réponses du modèle par rapport aux réponses attendues.
    
    Args:
        results_file: Chemin vers le fichier JSONL contenant les résultats du benchmark
    """
    if not os.path.exists(results_file):
        print(f"Le fichier {results_file} n'existe pas.")
        return
    
    print("\n=== Vérification des réponses ===")
    print(f"{'ID':^5} | {'Réponse attendue':^30} | {'Réponse du modèle':^30} | {'Résultat':^10}")
    print("-" * 80)
    
    with open(results_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                
                # Extraire les informations pertinentes
                if 'inputs' in data and 'example' in data['inputs'] and 'output' in data:
                    question_id = data['inputs']['example'].get('question_id', 'N/A')
                    expected = data['inputs']['example'].get('answer', 'N/A')
                    
                    # Extraire la réponse du modèle (après le <think> si présent)
                    model_output = data['output'].get('output', '')
                    if isinstance(model_output, str) and "</think>" in model_output:
                        model_output = model_output.split("</think>")[-1].strip()
                    
                    # Vérifier si la réponse est correcte
                    is_correct = data['output'].get('scores', {}).get('evaluate_as_python_objects', {}).get('exact_match', False)
                    result = "OK" if is_correct else "ERREUR"
                    
                    # Afficher les informations
                    print(f"{question_id:^5} | {expected[:30]:^30} | {model_output[:30]:^30} | {result:^10}")
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Erreur lors du traitement d'une ligne: {e}")
                continue

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_responses.py <results_file.jsonl>")
        sys.exit(1)
    
    verify_responses(sys.argv[1])