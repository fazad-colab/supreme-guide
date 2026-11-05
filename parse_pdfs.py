# Fichier : generer_cerveau_complet.py (v3 robuste)
import os
import json
import re

# --- Backends d'extraction (par ordre de préférence) ---
BACKENDS = []

try:
    import fitz  # PyMuPDF
    BACKENDS.append(("pymupdf", fitz))
except ImportError:
    fitz = None

try:
    from pypdf import PdfReader
    BACKENDS.append(("pypdf", PdfReader))
except ImportError:
    PdfReader = None

# --- OCR optionnel (si les PDF sont des scans) ---
try:
    import pytesseract
    from PIL import Image
    OCR_OK = True
except ImportError:
    OCR_OK = False


def nettoyer_texte(texte):
    texte = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', texte)
    texte = re.sub(r'\n{3,}', '\n\n', texte)
    return texte.strip()


def extraire_pymupdf(chemin):
    doc = fitz.open(chemin)
    total = []
    for i, page in enumerate(doc):
        t = page.get_text("text") or ""
        if t.strip():
            total.append(f"\n[Page {i+1}]\n{t}")
    doc.close()
    return "".join(total)


def extraire_pypdf(chemin):
    lecteur = PdfReader(chemin)
    if lecteur.is_encrypted:
        raise ValueError("PDF chiffré")
    total = []
    for i, page in enumerate(lecteur.pages):
        t = page.extract_text() or ""
        if t.strip():
            total.append(f"\n[Page {i+1}]\n{t}")
    return "".join(total)


def extraire_ocr(chemin, max_pages=20):
    """OCR lourd : à n'utiliser que sur les PDF scannés."""
    if not OCR_OK:
        return ""
    doc = fitz.open(chemin)
    total = []
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        pix = page.get_pixmap(dpi=200)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        try:
            t = pytesseract.image_to_string(img, lang="fra")
            if t.strip():
                total.append(f"\n[Page {i+1}]\n{t}")
        except Exception as e:
            print(f"   ⚠️ OCR page {i+1} : {e}")
    doc.close()
    return "".join(total)


def extraire_pdf(chemin):
    """Essaie chaque backend jusqu'à obtenir du texte."""
    for nom, _ in BACKENDS:
        try:
            if nom == "pymupdf":
                t = extraire_pymupdf(chemin)
            elif nom == "pypdf":
                t = extraire_pypdf(chemin)
            else:
                continue
            if len(t.strip()) > 100:
                return t, nom
        except Exception as e:
            print(f"   ⚠️ {nom} a échoué : {type(e).__name__}: {e}")
    # Dernier recours : OCR
    if OCR_OK and fitz is not None:
        print(f"   🔄 Tentative OCR (peut prendre du temps)...")
        t = extraire_ocr(chemin)
        if t.strip():
            return t, "ocr"
    return "", None


def generer_cerveau():
    cours_detectes = {}
    extensions_exclues = (".py", ".json", ".md", ".yml", ".git", ".jpg", ".png", ".tmp")

    print(f"🔧 Backends disponibles : {[b[0] for b in BACKENDS]}")
    print(f"🔧 OCR disponible : {OCR_OK}\n")

    for fichier in os.listdir("."):
        if fichier.startswith(".") or fichier.lower().endswith(extensions_exclues):
            continue

        nom_cle = fichier.replace("_", " ").replace("-", " ").lower()
        texte_integral = ""

        if fichier.lower().endswith(".pdf"):
            texte_integral, methode = extraire_pdf(fichier)
            if texte_integral:
                texte_integral = nettoyer_texte(texte_integral)
                print(f"✅ {fichier} : {len(texte_integral)} chars via {methode}")
            else:
                print(f"❌ {fichier} : AUCUN TEXTE (scan sans OCR ?)")

        mots_cles = [m for m in re.split(r'[\s_\-]+', nom_cle.replace(".pdf", "")) if len(m) > 2]
        if "analyse" in nom_cle:
            mots_cles.extend(["limite", "derivee", "integrale", "suite", "fonction", "convergence"])
        if "algebre" in nom_cle:
            mots_cles.extend(["matrice", "espace", "vectoriel", "polynome", "lineaire", "determinant"])
        if "algorithme" in nom_cle or "informatique" in nom_cle:
            mots_cles.extend(["code", "boucle", "fonction", "variable", "structure", "condition"])
        if "mecanique" in nom_cle or "mécanique" in nom_cle:
            mots_cles.extend(["force", "vitesse", "acceleration", "energie", "masse"])

        cours_detectes[nom_cle] = {
            "titre": fichier,
            "lien_cdn": f"https://cdn.jsdelivr.net/gh/fazad-colab/supreme-guide@main/{fichier.replace(' ', '%20')}",
            "mots_cles": sorted(set(mots_cles)),
            "contenu_integral": texte_integral[:15000]
        }

    cerveau = {
        "statut": "Généré avec extraction multi-backend (PyMuPDF/pypdf/OCR)",
        "cours": cours_detectes,
        "expressions_humaines": [
            "Franchement, bien vu !",
            "J'ai analysé les documents de supreme-guide, tout est dans les polycopiés.",
            "On lâche rien, la rigueur mathématique mène au sommet !"
        ]
    }

    with open("locki_brain.json", "w", encoding="utf-8") as f:
        json.dump(cerveau, f, ensure_ascii=False, indent=2)

    total_chars = sum(len(c['contenu_integral']) for c in cours_detectes.values())
    non_vides = sum(1 for c in cours_detectes.values() if c['contenu_integral'])
    print(f"\n🚀 locki_brain.json généré")
    print(f"   📚 {non_vides}/{len(cours_detectes)} PDF avec texte")
    print(f"   📝 {total_chars} caractères totaux")


if __name__ == "__main__":
    generer_cerveau()
