import json

# Fonction pour extraire le numéro de question à partir de l'ID
def extract_question_id(sample_id):
    return int(sample_id.replace("sample_", ""))

# Fonction pour formater le prompt en français
def format_prompt(code, input_data):
    return f"Étant donné la fonction suivante : `{code}` et l'entrée `{input_data}`, quelle est la sortie ?"

# Lire le fichier JSONL et le convertir
def convert_jsonl_to_json(input_file, output_file):
    eval_data = []
    
    # Lire le fichier JSONL ligne par ligne
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Parser chaque ligne comme un objet JSON
            data = json.loads(line.strip())
            
            # Extraire les champs nécessaires
            question_id = extract_question_id(data['id'])
            prompt = format_prompt(data['code'], data['input'])
            answer = data['output']
            
            # Créer l'objet pour eval_data
            eval_entry = {
                "question_id": question_id,
                "prompt": prompt,
                "answer": answer
            }
            
            eval_data.append(eval_entry)
    
    # Créer la structure JSON finale
    output_data = {"eval_data": eval_data}
    
    # Écrire dans le fichier de sortie
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

# Exécuter la conversion
if __name__ == "__main__":
    input_file = "./test.jsonl_copy.txt"
    output_file = "converted_code_bench.json"
    convert_jsonl_to_json(input_file, output_file)
    print(f"Conversion terminée. Le fichier JSON a été écrit dans {output_file}")