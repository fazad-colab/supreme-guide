import os
import json

def generer_cerveau():
    dossier_actuel = "."
    cours_detectes = {}
    
    # Parcourir tous les fichiers du dépôt
    for fichier in os.listdir(dossier_actuel):
        if fichier.endswith(".pdf"):
            nom_propre = fichier.replace(".pdf", "").replace("_", " ").lower()
            # Création d'une entrée intelligente pour chaque cours trouvé
            cours_detectes[nom_propre] = {
                "titre": fichier,
                "lien_cdn": f"https://cdn.jsdelivr.net/gh/fazad-colab/supreme-guide@main/{fichier}",
                "description": f"Document officiel de référence : {fichier}. À étudier pour valider les modules."
            }

    # Structure du cerveau final de Locki
    cerveau = {
        "statut": "Auto-généré par GitHub Actions",
        "cours": cours_detectes,
        "expressions_humaines": [
            "Franchement, bien vu !",
            "Regarde ce polycopié sur le dépôt, tout est détaillé dedans.",
            "On lâche rien, les partiels aux Comores se gagnent avec la rigueur !"
        ]
    }

    # Sauvegarde dans locki_brain.json
    with open("locki_brain.json", "w", encoding="utf-8") as f:
        json.dump(cerveau, f, ensure_ascii=False, indent=4)
    print("✅ Fichier locki_brain.json généré avec succès !")

if __name__ == "__main__":
    generer_cerveau()
