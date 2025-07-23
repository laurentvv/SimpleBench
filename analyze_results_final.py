#!/usr/bin/env python3
import json
import sys
import re
import textwrap

def normalize_code(code):
    """Normalisation avancée du code"""
    if not isinstance(code, str):
        return ""
    
    # Supprimer complètement les sections <think>...</think>
    think_pattern = r'<think>[\s\S]*?</think>'
    while re.search(think_pattern, code):
        code = re.sub(think_pattern, '', code)
    
    # Supprimer les backticks de code et les balises python
    code = re.sub(r'```python\n|```\n|```python|```', '', code)
    
    # Supprimer les définitions de fonction
    code = re.sub(r'^def\s+[^\(]+\([^\)]*\)\s*:\s*\n', '', code)
    
    # Supprimer les docstrings (multi-lignes et simples)
    code = re.sub(r'"""[\s\S]*?"""', '', code)
    code = re.sub(r"'''[\s\S]*?'''", '', code)
    
    try:
        # Essayer de détecter l'indentation et de normaliser le code
        lines = code.split('\n')
        
        # Ignorer les lignes vides pour la détection d'indentation
        non_empty_lines = [line for line in lines if line.strip()]
        if not non_empty_lines:
            return ""
        
        # Détecter l'indentation minimale (non vide)
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)
        
        # Normaliser l'indentation
        normalized_lines = []
        for line in lines:
            if line.strip():  # Ignorer les lignes vides
                # Supprimer l'indentation minimale
                if len(line) >= min_indent:
                    line = line[min_indent:]
                # Remplacer les tabulations par des espaces
                line = line.replace('\t', '    ')
                # Supprimer les espaces en fin de ligne
                line = line.rstrip()
                normalized_lines.append(line)
            elif normalized_lines:  # Conserver une seule ligne vide entre les lignes de code
                if not normalized_lines[-1] == '':
                    normalized_lines.append('')
        
        # Rejoindre les lignes
        code = '\n'.join(normalized_lines)
        
        # Essayer de reformater le code avec textwrap.dedent
        code = textwrap.dedent(code)
        
    except Exception:
        # En cas d'erreur, revenir à une normalisation simple
        code = '\n'.join(line.strip() for line in code.split('\n') if line.strip())
    
    # Supprimer les lignes vides au début et à la fin
    code = code.strip()
    
    return code

def analyze_results(results_file):
    """Analyse les résultats d'évaluation"""
    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\n=== Analyse des résultats d'évaluation ===\n")
    
    total = 0
    correct = 0
    basic_norm_matches = 0
    advanced_norm_matches = 0
    extreme_norm_matches = 0
    ast_matches = 0
    ai_equivalents = 0
    
    # Stocker les résultats pour chaque question
    results = []
    
    for item in data:
        # Ignorer les évaluations incomplètes
        if 'output' not in item or item['output'] is None:
            continue
                
        if 'inputs' in item and 'example' in item['inputs'] and 'output' in item['output']:
            question_id = item['inputs']['example'].get('question_id', 'N/A')
            expected = item['inputs']['example'].get('answer', '').strip()
            
            # Extraire la réponse du modèle
            model_output = item['output'].get('output', '')
            
            # Vérifier si la réponse a été validée et la raison
            is_valid = False
            reason = None
            
            if 'scores' in item['output']:
                scores = item['output']['scores']
                if 'score_function' in scores:
                    is_valid = scores['score_function'].get('exact_match', False)
                    reason = scores['score_function'].get('reason', None)
                elif 'evaluate_with_enhanced_approach' in scores:
                    is_valid = scores['evaluate_with_enhanced_approach'].get('exact_match', False)
                    reason = scores['evaluate_with_enhanced_approach'].get('reason', None)
                elif 'evaluate_as_python_objects' in scores:
                    is_valid = scores['evaluate_as_python_objects'].get('exact_match', False)
                elif 'evaluate_humaneval' in scores:
                    is_valid = scores['evaluate_humaneval'].get('exact_match', False)
            
            # Incrémenter les compteurs
            total += 1
            if is_valid:
                correct += 1
                if reason == 'basic_norm_match':
                    basic_norm_matches += 1
                elif reason == 'advanced_norm_match':
                    advanced_norm_matches += 1
                elif reason == 'extreme_norm_match':
                    extreme_norm_matches += 1
                elif reason == 'ast_match':
                    ast_matches += 1
                elif reason == 'ai_equivalent':
                    ai_equivalents += 1
            
            # Stocker les résultats pour cette question
            result = {
                'question_id': question_id,
                'is_correct': is_valid,
                'reason': reason,
                'expected': expected,
                'output': model_output
            }
            results.append(result)
    
    # Afficher les statistiques
    if total > 0:
        print(f"Total des questions évaluées: {total}")
        print(f"Réponses correctes: {correct}/{total} ({correct/total*100:.2f}%)")
        print(f"  - Normalisation basique: {basic_norm_matches}/{total} ({basic_norm_matches/total*100:.2f}%)")
        print(f"  - Normalisation avancée: {advanced_norm_matches}/{total} ({advanced_norm_matches/total*100:.2f}%)")
        print(f"  - Normalisation extrême: {extreme_norm_matches}/{total} ({extreme_norm_matches/total*100:.2f}%)")
        print(f"  - Comparaison AST: {ast_matches}/{total} ({ast_matches/total*100:.2f}%)")
        print(f"  - Équivalences IA: {ai_equivalents}/{total} ({ai_equivalents/total*100:.2f}%)")
    else:
        print("Aucune question évaluée.")
    
    # Afficher les réponses correctes
    print("\n=== Réponses correctes ===\n")
    
    for result in results:
        if result['is_correct']:
            print(f"Question {result['question_id']}: Correcte ({result['reason']})")
            print(f"  Attendu: {normalize_code(result['expected'])[:100]}...")
            print(f"  Reçu:    {normalize_code(result['output'])[:100]}...")
            print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_results_final.py <results_file.json>")
        sys.exit(1)
    
    analyze_results(sys.argv[1])