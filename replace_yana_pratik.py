"""
Script pour remplacer "Pratik" par "Pratik" dans tous les fichiers du projet
"""
import os
import re
from pathlib import Path

# Dossiers à exclure
EXCLUDE_DIRS = {
    'venv', '.venv', 'node_modules', 'staticfiles', 'htmlcov', 
    '__pycache__', '.git', '.pytest_cache', 'media'
}

# Extensions de fichiers à traiter
INCLUDE_EXTENSIONS = {
    '.py', '.html', '.md', '.txt', '.js', '.css', '.json', 
    '.yml', '.yaml', '.env', '.sh', '.bat'
}

def should_process_file(file_path):
    """Vérifie si le fichier doit être traité"""
    # Vérifier les dossiers exclus
    parts = Path(file_path).parts
    if any(excluded in parts for excluded in EXCLUDE_DIRS):
        return False
    
    # Vérifier l'extension
    if file_path.suffix not in INCLUDE_EXTENSIONS:
        return False
    
    return True

def replace_in_file(file_path):
    """Remplace 'Pratik' par 'Pratik' dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compter les occurrences
        count = content.count('Pratik')
        if count == 0:
            return 0
        
        # Remplacer
        new_content = content.replace('Pratik', 'Pratik')
        
        # Écrire le nouveau contenu
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return count
    except Exception as e:
        print(f"Erreur avec {file_path}: {e}")
        return 0

def main():
    """Fonction principale"""
    base_dir = Path('.')
    total_files = 0
    total_replacements = 0
    
    print("🔍 Recherche des fichiers contenant 'Pratik'...\n")
    
    # Parcourir tous les fichiers
    for file_path in base_dir.rglob('*'):
        if file_path.is_file() and should_process_file(file_path):
            count = replace_in_file(file_path)
            if count > 0:
                total_files += 1
                total_replacements += count
                print(f"✅ {file_path}: {count} remplacement(s)")
    
    print(f"\n{'='*60}")
    print(f"✨ Terminé !")
    print(f"📁 Fichiers modifiés: {total_files}")
    print(f"🔄 Remplacements effectués: {total_replacements}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
