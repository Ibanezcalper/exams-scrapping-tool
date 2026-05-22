import json
import re
import os
import hashlib

def get_hash(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

with open('examen_completo.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for exam_key, exam in data.items():
    for q_idx, q in enumerate(exam['preguntas']):
        if not q.get('explicacion'): continue
        
        expl = q['explicacion']
        
        # 1. FIX es_correcta
        match = re.search(r'(Opción correcta:|Opciones correctas:)(.*?)(Opciones incorrectas:|Opción incorrecta:|$)', expl, re.DOTALL | re.IGNORECASE)
        
        correct_indices = []
        if match:
            correct_block = match.group(2).strip()
            
            for opt_idx, opt in enumerate(q['opciones']):
                opt_text = opt['texto'].strip()
                if opt_text in correct_block:
                    correct_indices.append(opt_idx)
                else:
                    first_line = opt_text.split('\n')[0].strip()
                    if first_line and first_line in correct_block:
                        correct_indices.append(opt_idx)
            
            # Apply fixes
            if correct_indices:
                for opt_idx, opt in enumerate(q['opciones']):
                    opt['es_correcta'] = opt_idx in correct_indices

        # 2. DE-DUPLICATE & DISTRIBUTE IMAGES
        expl_imgs = q.get('imagenes_explicacion', [])
        unique_imgs = []
        seen_hashes = set()
        
        for img_path in expl_imgs:
            h = get_hash(img_path)
            if h and h not in seen_hashes:
                seen_hashes.add(h)
                unique_imgs.append(img_path)
            elif not h:
                # If file doesn't exist for some reason, keep it to be safe
                unique_imgs.append(img_path)
        
        # If number of unique images matches number of correct options, distribute!
        if correct_indices and len(unique_imgs) == len(correct_indices):
            for i, opt_idx in enumerate(correct_indices):
                if 'imagenes' not in q['opciones'][opt_idx]:
                    q['opciones'][opt_idx]['imagenes'] = []
                q['opciones'][opt_idx]['imagenes'].append(unique_imgs[i])
            q['imagenes_explicacion'] = [] # clear them from explanation
        else:
            # Just keep the deduplicated images in the explanation
            q['imagenes_explicacion'] = unique_imgs

# Save the fixed JSON
with open('examen_completo_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

