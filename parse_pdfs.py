import os
import json

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

def generer_cerveau():
    dossier_actuel = "."
    cours_detectes = {}
    
    # Extensions à ignorer (code source, scripts, etc.)
    extensions_exclues = (".py", ".json", ".md", ".yml", ".git")
    
    print("🔄 Analyse des fichiers du dépôt supreme-guide...")

    for fichier in os.listdir(dossier_actuel):
        if fichier.startswith(".") or fichier.endswith(extensions_exclues):
            continue
            
        nom_cle = fichier.replace("_", " ").replace("-", " ").lower()
        texte_integral = ""
        mots_cles = []

        # Extraction intelligente du texte si c'est un PDF
        if fichier.endswith(".pdf") and PdfReader is not None:
            try:
                lecteur = PdfReader(fichier)
                for i, page in enumerate(lecteur.pages):
                    t = page.extract_text()
                    if t:
                        texte_integral += f"\n--- Page {i+1} ---\n" + t
                print(f"✅ Texte extrait avec succès pour : {fichier} ({len(texte_integral)} caractères)")
            except Exception as e:
                print(f"⚠️ Erreur de lecture sur {fichier}: {e}")
                texte_integral = f"Document officiel : {fichier}"
        else:
            texte_integral = f"Fichier de référence : {fichier}"

        # Génération automatique de mots-clés pertinents basés sur le nom du fichier
        mots_cles = [m for m in nom_cle.replace(".pdf", "").split() if len(m) > 2]
        if "analyse" in nom_cle:
            mots_cles.extend(["limite", "derivee", "integrale", "suite", "fonction"])
        elif "algebre" in nom_cle:
            mots_cles.extend(["matrice", "espace", "vectoriel", "polynome", "lineaire"])
        elif "algorithme" in nom_cle or "informatique" in nom_cle:
            mots_cles.extend(["code", "boucle", "fonction", "variable", "structure"])

        # Enregistrement dans le dictionnaire structuré pour Locki
        cours_detectes[nom_cle] = {
            "titre": fichier,
            "lien_cdn": f"https://cdn.jsdelivr.net/gh/fazad-colab/supreme-guide@main/{fichier}",
            "mots_cles": list(set(mots_cles)),
            "contenu_integral": texte_integral.strip()
        }

    # Cerveau complet et structuré
    cerveau = {
        "statut": "Généré proprement avec extraction intégrale des cours",
        "cours": cours_detectes,
        "expressions_humaines": [
            "Franchement, bien vu !",
            "J'ai épluché le dépôt supreme-guide, tout est dans les documents officiels.",
            "On lâche rien, la rigueur mathématique et l'algorithmique mènent au Play Store !"
        ]
    }

    # Écriture finale dans locki_brain.json
    with open("locki_brain.json", "w", encoding="utf-8") as f:
        json.dump(cerveau, f, ensure_ascii=False, indent=4)
    
    print("🚀 Fichier locki_brain.json généré et prêt à être utilisé par Locki IA !")

if __name__ == "__main__":
    generer_cerveau()
