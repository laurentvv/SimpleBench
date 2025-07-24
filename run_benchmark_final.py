#!/usr/bin/env python3
import json
import weave
import asyncio
import os
import re
import ast
import textwrap
from fire import Fire
from dotenv import load_dotenv
load_dotenv()

from weave_utils.models import LiteLLMModel, MajorityVoteModel

# Prompts système optimisés pour chaque type de dataset
SYSTEM_PROMPTS = {
    "humaneval": """Vous êtes un assistant de programmation Python expert. Votre tâche est d'implémenter des fonctions Python selon les spécifications données.

Règles CRITIQUES à suivre STRICTEMENT :
1. Répondez UNIQUEMENT avec le corps de la fonction (le code indenté à l'intérieur de la fonction).
2. NE JAMAIS inclure la signature de la fonction (ligne commençant par "def").
3. NE JAMAIS inclure la docstring.
4. NE JAMAIS ajouter de commentaires ou d'explications.
5. NE JAMAIS entourer votre réponse de backticks (```python) ou de guillemets.
6. NE JAMAIS utiliser de balises <think> ou </think>.
7. Votre réponse doit commencer directement par le code indenté.""",

    "cruxeval": """Vous êtes un assistant expert en programmation et en résolution de problèmes. Votre objectif est de prédire la sortie d'un programme Python.

Règles à suivre :
1. Analysez le code fourni et l'entrée.
2. Déterminez la sortie exacte que le programme produira.
3. Répondez UNIQUEMENT avec la sortie, sans explication ni formatage supplémentaire.""",
    
    "code_x_glue": """Vous êtes un assistant expert en programmation. Votre tâche est de générer une description en langage naturel pour un morceau de code Python.

Règles à suivre :
1. Lisez et comprenez la fonctionnalité du code fourni.
2. Décrivez le but et le fonctionnement du code en français.
3. Votre réponse doit être une description claire et concise."""
}

# Prompt pour l'évaluation par IA
AI_EVALUATOR_PROMPT = """Vous êtes un évaluateur expert en programmation Python. Votre tâche est de déterminer si deux implémentations de fonction sont fonctionnellement équivalentes.

Voici la solution attendue :
```python
{expected}
```

Voici la solution proposée :
```python
{actual}
```

Analysez attentivement les deux implémentations et déterminez si elles sont fonctionnellement équivalentes, c'est-à-dire si elles produisent les mêmes résultats pour les mêmes entrées.

Ignorez les différences de style, de noms de variables, d'indentation ou de formatage. Concentrez-vous uniquement sur la fonctionnalité.

Répondez UNIQUEMENT par "EQUIVALENT" ou "NON_EQUIVALENT", suivi d'une brève explication.
"""

def normalize_code_basic(code):
    """Normalisation basique du code"""
    if not isinstance(code, str):
        return ""
    
    # Supprimer les balises <think>...</think>
    code = re.sub(r'<think>[\s\S]*?</think>', '', code).strip()
    
    # Supprimer les backticks de code et les balises python
    code = re.sub(r'```python\n|```\n|```python|```', '', code)
    
    # Supprimer les définitions de fonction
    code = re.sub(r'^def\s+[^\(]+\([^\)]*\)\s*:\s*\n', '', code)
    
    # Supprimer les docstrings
    code = re.sub(r'"""[^"]*"""\n', '', code)
    code = re.sub(r"'''[^']*'''\n", '', code)
    
    # Normaliser les espaces et les indentations
    lines = code.split('\n')
    normalized_lines = []
    for line in lines:
        # Remplacer les tabulations par des espaces
        line = line.replace('\t', '    ')
        # Supprimer les espaces en fin de ligne
        line = line.rstrip()
        normalized_lines.append(line)
    
    # Rejoindre les lignes
    code = '\n'.join(normalized_lines)
    
    # Supprimer les lignes vides au début et à la fin
    code = code.strip()
    
    return code

def normalize_code_advanced(code):
    """Normalisation avancée du code"""
    if not isinstance(code, str):
        return ""
    
    # Supprimer complètement les sections <think>...</think>
    # Utilisation d'une regex plus robuste pour gérer les balises imbriquées
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

def normalize_code_extreme(code):
    """Normalisation extrême du code (supprime tous les espaces et sauts de ligne)"""
    if not isinstance(code, str):
        return ""
    
    # Normaliser d'abord avec la méthode avancée
    code = normalize_code_advanced(code)
    
    # Supprimer tous les espaces et sauts de ligne
    code = re.sub(r'\s+', '', code)
    
    return code

def compare_ast_structures(code1, code2):
    """Compare la structure AST de deux codes Python"""
    try:
        # Ajouter une indentation pour que le code soit valide
        indented_code1 = "def func():\n" + "\n".join("    " + line for line in code1.split("\n"))
        indented_code2 = "def func():\n" + "\n".join("    " + line for line in code2.split("\n"))
        
        # Parser les AST
        ast1 = ast.parse(indented_code1)
        ast2 = ast.parse(indented_code2)
        
        # Classe pour normaliser les noms de variables dans l'AST
        class NameNormalizer(ast.NodeTransformer):
            def __init__(self):
                self.name_map = {}
                self.counter = 0
            
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store):
                    if node.id not in self.name_map:
                        self.name_map[node.id] = f"var_{self.counter}"
                        self.counter += 1
                if node.id in self.name_map:
                    node.id = self.name_map[node.id]
                return node
        
        # Normaliser les noms de variables
        normalizer1 = NameNormalizer()
        normalizer2 = NameNormalizer()
        
        ast1 = normalizer1.visit(ast1)
        ast2 = normalizer2.visit(ast2)
        
        # Comparer les AST normalisés
        return ast.dump(ast1, annotate_fields=False) == ast.dump(ast2, annotate_fields=False)
    except Exception:
        return False

# Fonction pour détecter automatiquement le type de dataset
def detect_dataset_type(source_path):
    """Détecte automatiquement le type de dataset basé sur le nom du fichier"""
    filename = os.path.basename(source_path).lower()
    
    if "humaneval" in filename:
        return "humaneval"
    elif "cruxeval" in filename:
        return "cruxeval"
    elif "code-x-glue" in filename or "code_x_glue" in filename:
        return "code_x_glue"
    else:
        # Par défaut, on essaie de détecter en fonction du contenu
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line.startswith('['):
                    # Probablement un JSON array (HumanEval ou Code-X-GLUE)
                    data = json.loads(first_line + f.read())
                    if isinstance(data, list) and len(data) > 0:
                        if "task_id" in data[0] and "canonical_solution" in data[0]:
                            return "humaneval"
                        elif "code" in data[0] and "nl" in data[0]:
                            return "code_x_glue"
                elif first_line.startswith('{'):
                    # Probablement un JSONL (CruxEval)
                    return "cruxeval"
        except:
            pass
        
        # Si on ne peut pas détecter, on utilise un format générique
        return "generic"

# Fonctions de chargement de datasets
def load_humaneval_dataset(source_path):
    """Charge un dataset HumanEval depuis sa source originale"""
    with open(source_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    eval_data = []
    for i, problem in enumerate(data):
        task_id = problem.get('task_id', f"task_{i}")
        question_id = int(task_id.split('/')[1]) if '/' in task_id else i
        prompt_text = problem.get('prompt', '')
        solution = problem.get('canonical_solution', '').strip()
        
        # Formater le prompt pour demander uniquement le corps de la fonction
        function_name = None
        for line in prompt_text.split("\n"):
            if line.strip().startswith("def "):
                function_name = line.strip().split("(")[0].replace("def ", "").strip()
                break
        
        prompt = f"""Définissez le corps de la fonction {function_name} décrite ci-dessous. Retournez UNIQUEMENT le corps de la fonction, sans la signature ni la docstring.

```python
{prompt_text}
```"""
        
        eval_entry = {
            "question_id": question_id,
            "prompt": prompt,
            "answer": solution
        }
        
        eval_data.append(eval_entry)
    
    return eval_data

def load_cruxeval_dataset(source_path):
    """Charge un dataset CruxEval depuis sa source originale"""
    eval_data = []
    
    # Détecter si c'est un fichier JSON ou JSONL
    with open(source_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        f.seek(0)  # Revenir au début du fichier
        
        if first_line.startswith('['):
            # Format JSON
            data = json.load(f)
            for i, item in enumerate(data):
                code = item.get('code', '')
                input_data = item.get('input', '')
                output = item.get('output', '')
                question_id = i
                
                prompt = f"Étant donné la fonction suivante : `{code}` et l'entrée `{input_data}`, quelle est la sortie ?"
                
                eval_entry = {
                    "question_id": question_id,
                    "prompt": prompt,
                    "answer": output
                }
                
                eval_data.append(eval_entry)
        else:
            # Format JSONL
            for i, line in enumerate(f):
                try:
                    data = json.loads(line.strip())
                    code = data.get('code', '')
                    input_data = data.get('input', '')
                    output = data.get('output', '')
                    question_id = i
                    
                    prompt = f"Étant donné la fonction suivante : `{code}` et l'entrée `{input_data}`, quelle est la sortie ?"
                    
                    eval_entry = {
                        "question_id": question_id,
                        "prompt": prompt,
                        "answer": output
                    }
                    
                    eval_data.append(eval_entry)
                except:
                    continue
    
    return eval_data

def load_code_x_glue_dataset(source_path):
    """Charge un dataset Code-X-GLUE depuis sa source originale"""
    with open(source_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    eval_data = []
    for i, item in enumerate(data):
        code = item.get('code', '')
        nl = item.get('nl', '')  # Description en langage naturel
        
        prompt = f"Décrivez ce que fait le code suivant en français :\n\n```\n{code}\n```"
        
        eval_entry = {
            "question_id": i,
            "prompt": prompt,
            "answer": nl
        }
        
        eval_data.append(eval_entry)
    
    return eval_data

def load_dataset_from_source(source_path, dataset_type=None):
    """Charge un dataset depuis sa source originale"""
    # Détection automatique du type si non spécifié
    if dataset_type is None:
        dataset_type = detect_dataset_type(source_path)
    
    print(f"Chargement du dataset de type: {dataset_type}")
    
    # Chargement selon le type
    if dataset_type == "humaneval":
        return load_humaneval_dataset(source_path)
    elif dataset_type == "cruxeval":
        return load_cruxeval_dataset(source_path)
    elif dataset_type == "code_x_glue":
        return load_code_x_glue_dataset(source_path)
    else:
        raise ValueError(f"Type de dataset non supporté: {dataset_type}")

@weave.op()
async def evaluate_code_final(answer: str, output: str, evaluator_model) -> dict:
    """
    Évalue la réponse du modèle avec une méthode complète qui combine:
    1. Comparaison exacte après normalisation basique
    2. Comparaison exacte après normalisation avancée
    3. Comparaison exacte après normalisation extrême
    4. Comparaison AST
    5. Évaluation par IA
    """
    # Vérifier si le modèle a atteint sa limite
    if output is None:
        return {'exact_match': False, 'reason': 'model_limit_reached'}
    
    # 1. Normalisation basique
    norm_expected_basic = normalize_code_basic(answer)
    norm_output_basic = normalize_code_basic(output)
    
    if norm_expected_basic == norm_output_basic:
        return {'exact_match': True, 'reason': 'basic_norm_match'}
    
    # 2. Normalisation avancée
    norm_expected_advanced = normalize_code_advanced(answer)
    norm_output_advanced = normalize_code_advanced(output)
    
    if norm_expected_advanced == norm_output_advanced:
        return {'exact_match': True, 'reason': 'advanced_norm_match'}
    
    # 3. Normalisation extrême
    norm_expected_extreme = normalize_code_extreme(answer)
    norm_output_extreme = normalize_code_extreme(output)
    
    if norm_expected_extreme == norm_output_extreme:
        return {'exact_match': True, 'reason': 'extreme_norm_match'}
    
    # 4. Comparaison AST
    if compare_ast_structures(norm_expected_advanced, norm_output_advanced):
        return {'exact_match': True, 'reason': 'ast_match'}
    
    # 5. Évaluation par IA
    try:
        # Préparer le prompt pour l'évaluateur
        prompt = AI_EVALUATOR_PROMPT.format(
            expected=norm_expected_advanced,
            actual=norm_output_advanced
        )
        
        # Utiliser le modèle pour l'évaluation
        response = await evaluator_model.predict(prompt)
        
        # Analyser la réponse
        if "EQUIVALENT" in response and "NON_EQUIVALENT" not in response:
            return {'exact_match': True, 'reason': 'ai_equivalent'}
    except Exception as e:
        print(f"Erreur lors de l'évaluation par IA: {e}")
    
    # Si toutes les méthodes échouent, la réponse est incorrecte
    return {'exact_match': False, 'reason': 'not_equivalent'}

def run_benchmark(
    model_name: str = "qwen3:14b",
    dataset_source: str = "./sql-console-for-openai-openai-humaneval.json",
    dataset_type: str = None,
    num_responses: int = 1,
    entity: str = "laurentvv-none",
    project: str = "simple_bench",
    temp: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.95,
    max_retries: int = 3,
    custom_system_prompt: str = None,
):
    """
    Exécute un benchmark d'évaluation sur un modèle et un dataset donnés,
    avec une évaluation complète qui combine plusieurs méthodes.

    Args:
        model_name (str): Nom du modèle à utiliser pour l'inférence.
            Par défaut "qwen3:14b".
        dataset_source (str): Chemin vers le fichier source du dataset.
            Par défaut "./sql-console-for-openai-openai-humaneval.json".
        dataset_type (str): Type de dataset (humaneval, cruxeval, code_x_glue).
            Par défaut None (détection automatique).
        num_responses (int): Si supérieur à 1, le vote majoritaire sera appliqué.
            Par défaut 1 (pas de vote majoritaire).
        entity (str): Entité Weave optionnelle (nom d'org/utilisateur) pour le suivi de l'évaluation.
        project (str): Nom du projet sous l'entité spécifiée.
            Par défaut "simple_bench".
        temp (float): Température pour le modèle.
            Par défaut 0.7.
        max_tokens (int): Nombre maximum de tokens à générer.
            Par défaut 2048.
        top_p (float): Top-p pour le modèle.
            Par défaut 0.95.
        max_retries (int): Nombre maximum de tentatives en cas d'erreur.
            Par défaut 3.
        custom_system_prompt (str): Prompt système personnalisé pour le modèle.
            Par défaut None (utilise le prompt par défaut pour le type de dataset).

    Exemple:
        python run_benchmark_final.py --model_name=qwen3:14b --dataset_source=sql-console-for-openai-openai-humaneval.json
    """
    # Détecter automatiquement le type de dataset si non spécifié
    if dataset_type is None:
        dataset_type = detect_dataset_type(dataset_source)
    
    if entity is not None:
        weave.init(f"{entity}/{project}")
    else:
        weave.init(f"{project}")
    
    # Charger le dataset
    dataset = load_dataset_from_source(dataset_source, dataset_type)
    
    # Obtenir le prompt système approprié
    system_prompt = custom_system_prompt
    if system_prompt is None:
        system_prompt = SYSTEM_PROMPTS.get(dataset_type, "Vous êtes un assistant expert. Répondez de manière précise et concise.")
    
    print(f"Utilisation du prompt système pour le dataset de type {dataset_type}")
    
    # Créer le modèle principal
    model = LiteLLMModel(
        model_name=model_name,
        temp=temp,
        max_tokens=max_tokens,
        top_p=top_p,
        max_retries=max_retries,
        system_prompt=system_prompt
    )
    
    if num_responses > 1:
        model = MajorityVoteModel(model=model, num_responses=num_responses)
    
    # Créer un modèle pour l'évaluation avec une température plus basse
    evaluator_model = LiteLLMModel(
        model_name=model_name,
        temp=0.1,  # Température plus basse pour des réponses plus déterministes
        max_tokens=500,
        top_p=0.95,
        max_retries=max_retries,
        system_prompt="Vous êtes un évaluateur expert en programmation Python."
    )
    
    # Définir la fonction de scoring
    @weave.op()
    def score_function(answer: str, output: str) -> dict:
        """Fonction de scoring qui utilise evaluate_code_final"""
        return asyncio.run(evaluate_code_final(answer, output, evaluator_model))
    
    # Créer l'évaluation
    evaluation = weave.Evaluation(
        dataset=dataset,
        scorers=[score_function],
        trials=1,
    )
    
    print(f"Démarrage de l'évaluation avec le modèle {model_name}...")
    result = asyncio.run(evaluation.evaluate(model))
    
    # Afficher les résultats
    print("\n=== Résultats de l'évaluation ===\n")
    print(result)
    
    # Calculer et afficher les statistiques
    total = 0
    correct = 0
    basic_norm_matches = 0
    advanced_norm_matches = 0
    extreme_norm_matches = 0
    ast_matches = 0
    ai_equivalents = 0
    
    # Récupérer les résultats
    exact_match_counts = result.get('score_function', {}).get('exact_match', {}).get('counts', [])
    reason_values = result.get('score_function', {}).get('reason', {}).get('values', [])
    
    total = len(exact_match_counts)
    
    for i, is_match in enumerate(exact_match_counts):
        if is_match and i < len(reason_values):
            correct += 1
            reason = reason_values[i]
            if reason == "basic_norm_match":
                basic_norm_matches += 1
            elif reason == "advanced_norm_match":
                advanced_norm_matches += 1
            elif reason == "extreme_norm_match":
                extreme_norm_matches += 1
            elif reason == "ast_match":
                ast_matches += 1
            elif reason == "ai_equivalent":
                ai_equivalents += 1
    
    if total > 0:
        print(f"\nRésultat final: {correct}/{total} correct ({correct/total*100:.2f}%)")
        print(f"  - Normalisation basique: {basic_norm_matches}/{total} ({basic_norm_matches/total*100:.2f}%)")
        print(f"  - Normalisation avancée: {advanced_norm_matches}/{total} ({advanced_norm_matches/total*100:.2f}%)")
        print(f"  - Normalisation extrême: {extreme_norm_matches}/{total} ({extreme_norm_matches/total*100:.2f}%)")
        print(f"  - Comparaison AST: {ast_matches}/{total} ({ast_matches/total*100:.2f}%)")
        print(f"  - Équivalences IA: {ai_equivalents}/{total} ({ai_equivalents/total*100:.2f}%)")
    else:
        print("\nAucune question évaluée.")

if __name__ == "__main__":
    Fire(run_benchmark)