import os
import json
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

def generer_cerveau():
    dossier_actuel = "."
    cours_detectes = {}
    
    # Extensions à exclure (scripts de code, configuration, etc.)
    extensions_exclues = (".py", ".json", ".md", ".yml", ".git")
    
    # Parcourir tous les fichiers du dépôt
    for fichier in os.listdir(dossier_actuel):
        if fichier.startswith(".") or fichier.endswith(extensions_exclues):
            continue
            
        nom_cle = fichier.replace("_", " ").replace("-", " ").lower()
        contenu_texte = ""
        
        # Extraction du texte si c'est un PDF et que la bibliothèque pypdf est disponible
        if fichier.endswith(".pdf") and PdfReader is not None:
            try:
                lecteur = PdfReader(fichier)
                for page in lecteur.pages:
                    texte_page = page.extract_text()
                    if texte_page:
                        contenu_texte += texte_page + "\n"
            except Exception as e:
                contenu_texte = f"Erreur de lecture du PDF : {str(e)}"
        
        # Si ce n'est pas un PDF ou si pypdf n'est pas dispo, on met une description de base
        if not contenu_texte:
            contenu_texte = f"Document de référence officiel : {fichier}"

        # Stockage dans le dictionnaire avec le texte intégral extrait
        cours_detectes[nom_cle] = {
            "titre": fichier,
            "lien_cdn": f"https://cdn.jsdelivr.net/gh/fazad-colab/supreme-guide@main/{fichier}",
            "contenu_integral": contenu_texte.strip()
        }

    # Structure complète du cerveau de Locki avec le contenu extrait
    cerveau = {
        "statut": "Généré automatiquement avec extraction de texte",
        "cours": cours_detectes,
        "expressions_humaines": [
            "Franchement, bien vu !",
            "J'ai analysé les documents du dépôt, tout est dedans.",
            "On lâche rien, la rigueur mathématique finit toujours par payer !"
        ]
    }

    # Sauvegarde dans locki_brain.json
    with open("locki_brain.json", "w", encoding="utf-8") as f:
        json.dump(cerveau, f, ensure_ascii=False, indent=4)
    print("✅ Fichier locki_brain.json généré avec succès avec le texte intégral des cours !")

if __name__ == "__main__":
    generer_cerveau()
