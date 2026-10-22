#!/usr/bin/env python3
"""Vérifie daily.json : structure, date, et nombre de mots par niveau.

Usage : python3 outils/verifier_daily.py daily.json [AAAA-MM-JJ]
Code de sortie 0 si tout est valide, 1 sinon (le détail est affiché).
"""
import json
import re
import sys
import unicodedata

# Niveau : (durée en s, débit en mots/min) — identique à LEVELS dans index.html
NIVEAUX = {
    "1": (60, 130),
    "2": (60, 145),
    "3": (90, 150),
    "4": (120, 155),
    "5": (180, 160),
}
TOL_BAS, TOL_HAUT = 0.93, 1.05


def norm(mot: str) -> str:
    mot = mot.lower().replace("œ", "oe").replace("æ", "ae")
    mot = unicodedata.normalize("NFD", mot)
    mot = "".join(c for c in mot if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", mot)


def compter(texte: str) -> int:
    return sum(1 for m in texte.split() if norm(m))


def main() -> int:
    chemin = sys.argv[1] if len(sys.argv) > 1 else "daily.json"
    date_attendue = sys.argv[2] if len(sys.argv) > 2 else None
    erreurs = []
    with open(chemin, encoding="utf-8") as f:
        data = json.load(f)
    if date_attendue and data.get("date") != date_attendue:
        erreurs.append(f"date = {data.get('date')!r}, attendu {date_attendue!r}")
    niveaux = data.get("levels", {})
    for n, (duree, debit) in NIVEAUX.items():
        bloc = niveaux.get(n)
        if not bloc:
            erreurs.append(f"niveau {n} absent")
            continue
        for champ in ("titre", "theme", "texte"):
            if not isinstance(bloc.get(champ), str) or not bloc[champ].strip():
                erreurs.append(f"niveau {n} : champ {champ} vide")
        cible = round(debit * duree / 60)
        bas, haut = round(cible * TOL_BAS), round(cible * TOL_HAUT)
        nb = compter(bloc.get("texte", ""))
        etat = "ok" if bas <= nb <= haut else "HORS CIBLE"
        print(f"niveau {n} : {nb} mots (cible {cible}, accepté {bas}-{haut}) {etat}")
        if etat != "ok":
            erreurs.append(f"niveau {n} : {nb} mots hors de {bas}-{haut}")
        if re.search(r"\d", bloc.get("texte", "")):
            erreurs.append(f"niveau {n} : chiffres présents, écrire les nombres en lettres")
    for e in erreurs:
        print("ERREUR :", e)
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
