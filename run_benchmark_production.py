#!/usr/bin/env python3
import json
import weave
import asyncio
import os
import re
import ast
import textwrap
import time
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
    
    "code_x_glue": """Vous êtes un assistant expert en programmation. Votre tâche est de générer une description en langage naturel pour un morceau de code.

Règles à suivre :
1. Lisez et comprenez la fonctionnalité du code fourni (peu importe le langage de programmation).
2. Décrivez le but et le fonctionnement du code de manière claire et concise.
3. Votre réponse doit être une description technique précise mais accessible.
4. NE PAS mentionner le langage de programmation dans votre réponse.
5. Concentrez-vous sur la FONCTIONNALITÉ, pas sur la syntaxe."""
}

# Prompts pour l'évaluation par IA selon le type de dataset
AI_EVALUATOR_PROMPTS = {
    "code": """Vous êtes un évaluateur expert en programmation. Votre tâche est de déterminer si deux implémentations de fonction sont fonctionnellement équivalentes.

Voici la solution attendue :
```
{expected}
```

Voici la solution proposée :
```
{actual}
```

Analysez attentivement les deux implémentations et déterminez si elles sont fonctionnellement équivalentes, c'est-à-dire si elles produisent les mêmes résultats pour les mêmes entrées.

Ignorez les différences de style, de noms de variables, d'indentation ou de formatage. Concentrez-vous uniquement sur la fonctionnalité.

Répondez UNIQUEMENT par "EQUIVALENT" ou "NON_EQUIVALENT", suivi d'une brève explication.""",
    
    "description": """Vous êtes un évaluateur expert en analyse de texte. Votre tâche est de déterminer si deux descriptions de code sont sémantiquement équivalentes.

Voici la description attendue :
{expected}

Voici la description proposée :
{actual}

Analysez attentivement les deux descriptions et déterminez si elles décrivent la même fonctionnalité de manière équivalente.

Ignorez les différences de style, de formulation ou de structure. Concentrez-vous uniquement sur le sens et la fonctionnalité décrite.

Répondez UNIQUEMENT par "EQUIVALENT" ou "NON_EQUIVALENT", suivi d'une brève explication."""
}

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
        # Utiliser la docstring comme réponse attendue
        docstring = item.get('docstring', '')
        
        # Nettoyer la docstring des marqueurs de commentaires
        if docstring.startswith('//'):
            docstring = docstring[2:].strip()
        
        prompt = f"Décrivez ce que fait le code suivant :\n\n```\n{code}\n```"
        
        eval_entry = {
            "question_id": i,
            "prompt": prompt,
            "answer": docstring
        }
        
        eval_data.append(eval_entry)
    
    return eval_data

def load_dataset_from_source(source_path, dataset_type=None):
    """Charge un dataset depuis sa source originale"""
    if dataset_type is None:
        dataset_type = detect_dataset_type(source_path)
    
    print(f"Chargement du dataset de type: {dataset_type}")
    
    if dataset_type == "humaneval":
        return load_humaneval_dataset(source_path)
    elif dataset_type == "cruxeval":
        return load_cruxeval_dataset(source_path)
    elif dataset_type == "code_x_glue":
        return load_code_x_glue_dataset(source_path)
    else:
        raise ValueError(f"Type de dataset non supporté: {dataset_type}")

@weave.op()
async def evaluate_code_final(answer: str, output: str, evaluator_model, dataset_type: str = "code") -> dict:
    """Évalue la réponse du modèle avec une méthode complète"""
    if output is None:
        return {'exact_match': False, 'reason': 'model_limit_reached'}
    
    # 1. Normalisation basique
    if normalize_code_basic(answer) == normalize_code_basic(output):
        return {'exact_match': True, 'reason': 'basic_norm_match'}
    
    # 2. Normalisation avancée
    if normalize_code_advanced(answer) == normalize_code_advanced(output):
        return {'exact_match': True, 'reason': 'advanced_norm_match'}
    
    # 3. Normalisation extrême
    if normalize_code_extreme(answer) == normalize_code_extreme(output):
        return {'exact_match': True, 'reason': 'extreme_norm_match'}
    
    # 4. Comparaison AST
    if compare_ast_structures(normalize_code_advanced(answer), normalize_code_advanced(output)):
        return {'exact_match': True, 'reason': 'ast_match'}
    
    # 5. Évaluation par IA
    try:
        prompt_type = "description" if dataset_type == "code_x_glue" else "code"
        ai_prompt = AI_EVALUATOR_PROMPTS[prompt_type].format(
            expected=answer, actual=output
        )
        response = await evaluator_model.predict(ai_prompt)
        
        if "EQUIVALENT" in response and "NON_EQUIVALENT" not in response:
            return {'exact_match': True, 'reason': 'ai_equivalent'}
    except Exception as e:
        print(f"Erreur lors de l'évaluation par IA: {e}")
    
    return {'exact_match': False, 'reason': 'not_equivalent'}

def run_benchmark(
    model_name: str = "qwen3:14b",
    dataset_source: str = "./sql-console-for-openai-openai-humaneval.json",
    dataset_type: str = None,
    num_responses: int = 1,
    entity: str = "laurentvv-none",
    project: str = "simple_bench",
    temp: float = 0.1,
    max_tokens: int = 2048,
    top_p: float = 0.95,
    max_retries: int = 3,
    custom_system_prompt: str = None,
):
    """
    Exécute un benchmark d'évaluation sur un modèle et un dataset donnés.
    """
    start_time = time.time()
    
    if dataset_type is None:
        dataset_type = detect_dataset_type(dataset_source)
    
    if entity is not None:
        weave.init(f"{entity}/{project}")
    else:
        weave.init(f"{project}")
    
    dataset = load_dataset_from_source(dataset_source, dataset_type)
    
    system_prompt = custom_system_prompt
    if system_prompt is None:
        system_prompt = SYSTEM_PROMPTS.get(dataset_type, "Vous êtes un assistant expert. Répondez de manière précise et concise.")
    
    print(f"Utilisation du prompt système pour le dataset de type {dataset_type}")
    
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
    
    evaluator_model = LiteLLMModel(
        model_name=model_name,
        temp=0.1,
        max_tokens=500,
        top_p=0.95,
        max_retries=max_retries,
        system_prompt="Vous êtes un évaluateur expert en programmation."
    )
    
    @weave.op()
    def score_function(answer: str, output: str) -> dict:
        return asyncio.run(evaluate_code_final(answer, output, evaluator_model, dataset_type))
    
    evaluation = weave.Evaluation(
        dataset=dataset,
        scorers=[score_function],
        trials=1,
    )
    
    print(f"Démarrage de l'évaluation avec le modèle {model_name}...")
    result = asyncio.run(evaluation.evaluate(model))
    
    print("\n=== Résultats de l'évaluation ===\n")
    print(result)
    
    try:
        score_data = result.get('score_function', {}) if result else {}
        exact_match_data = score_data.get('exact_match', {}) if score_data else {}
        
        total = exact_match_data.get('true_count', 0) + exact_match_data.get('false_count', 0)
        correct = exact_match_data.get('true_count', 0)
        elapsed = time.time() - start_time
        
        if total > 0:
            print(f"\nRésultat final: {correct}/{total} correct ({correct/total*100:.2f}%)")
            print(f"Temps d'exécution: {elapsed:.1f}s")
            
            try:
                import winsound
                for _ in range(3):
                    winsound.Beep(1000, 500)
            except (ImportError, Exception):
                # Fallback avec beep système
                for _ in range(5):
                    print("\a", end="", flush=True)
                print("\n🔔 Benchmark terminé !")
                # Alternative avec os.system
                try:
                    import os
                    os.system('echo \a')
                except:
                    pass
        else:
            print("\nAucune question évaluée.")
    except Exception as e:
        print(f"Erreur lors du calcul des statistiques: {e}")

if __name__ == "__main__":
    Fire(run_benchmark)