# Fichier : generer_cerveau_complet.py (version corrigée)
import os
import json
import re

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
    print("⚠️ pypdf non installé. Lance : pip install pypdf")

def nettoyer_texte(texte):
    """Enlève les sauts de ligne excessifs et les caractères de contrôle."""
    texte = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', texte)
    texte = re.sub(r'\n{3,}', '\n\n', texte)
    return texte.strip()

def generer_cerveau():
    dossier_actuel = "."
    cours_detectes = {}
    extensions_exclues = (".py", ".json", ".md", ".yml", ".git", ".jpg", ".png", ".tmp")

    print("🔄 Analyse des documents académiques du dépôt supreme-guide...")

    for fichier in os.listdir(dossier_actuel):
        if fichier.startswith(".") or fichier.lower().endswith(extensions_exclues):
            continue

        nom_cle = fichier.replace("_", " ").replace("-", " ").lower()
        texte_integral = ""

        # Extraction réelle du texte des PDF
        if fichier.lower().endswith(".pdf") and PdfReader is not None:
            try:
                lecteur = PdfReader(fichier)
                for i, page in enumerate(lecteur.pages):
                    t = page.extract_text() or ""
                    if t.strip():
                        texte_integral += f"\n[Page {i+1}]\n{t}"
                texte_integral = nettoyer_texte(texte_integral)
                print(f"✅ {fichier} : {len(texte_integral)} caractères extraits")
            except Exception as e:
                print(f"⚠️ Échec extraction {fichier}: {e}")
                texte_integral = ""
        else:
            texte_integral = ""

        # Mots-clés automatiques
        mots_cles = [m for m in re.split(r'[\s_\-]+', nom_cle.replace(".pdf", "")) if len(m) > 2]
        if "analyse" in nom_cle:
            mots_cles.extend(["limite", "derivee", "integrale", "suite", "fonction", "convergence"])
        if "algebre" in nom_cle:
            mots_cles.extend(["matrice", "espace", "vectoriel", "polynome", "lineaire", "determinant"])
        if "algorithme" in nom_cle or "informatique" in nom_cle:
            mots_cles.extend(["code", "boucle", "fonction", "variable", "structure", "condition"])
        if "mecanique" in nom_cle or "mécanique" in nom_cle:
            mots_cles.extend(["force", "vitesse", "acceleration", "energie", "masse"])
        if "probabilite" in nom_cle or "probabilité" in nom_cle:
            mots_cles.extend(["probabilite", "evenement", "variable", "aleatoire", "esperance"])

        cours_detectes[nom_cle] = {
            "titre": fichier,
            "lien_cdn": f"https://cdn.jsdelivr.net/gh/fazad-colab/supreme-guide@main/{fichier.replace(' ', '%20')}",
            "mots_cles": sorted(set(mots_cles)),
            "contenu_integral": texte_integral[:15000]  # limite pour ne pas alourdir le JSON
        }

    cerveau = {
        "statut": "Généré avec extraction intégrale via pypdf",
        "cours": cours_detectes,
        "expressions_humaines": [
            "Franchement, bien vu !",
            "J'ai analysé les documents de supreme-guide, tout est dans les polycopiés.",
            "On lâche rien, la rigueur mathématique mène au sommet !"
        ]
    }

    with open("locki_brain.json", "w", encoding="utf-8") as f:
        json.dump(cerveau, f, ensure_ascii=False, indent=2)
    print(f"🚀 locki_brain.json généré ({len(cours_detectes)} cours, {sum(len(c['contenu_integral']) for c in cours_detectes.values())} caractères totaux)")

if __name__ == "__main__":
    generer_cerveau()
