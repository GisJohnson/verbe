# Verbe — prompteur d'éloquence

Prompteur d'entraînement à la diction et à l'éloquence en français, avec suivi vocal, durées au choix (1:00 minimum) et cinq niveaux.

- `index.html` : l'application (une seule page, sans dépendance serveur). Ouvrir dans Chrome sur Android et autoriser le micro.
- `daily.json` : le script du jour, un par niveau. Réécrit chaque matin par une tâche programmée.
- `archives/AAAA-MM-JJ.json` : copie de chaque script du jour.
- `outils/verifier_daily.py` : contrôle la structure et le nombre de mots de `daily.json`.

## Niveaux

| Niveau | Nom | Durée | Débit visé |
|---|---|---|---|
| 1 | Fluidité | 1:00 | 130 mots/min |
| 2 | Liaisons | 1:00 | 145 mots/min |
| 3 | Sons difficiles | 1:30 | 150 mots/min |
| 4 | Virelangues | 2:00 | 155 mots/min |
| 5 | Rhétorique | 3:00 | 160 mots/min |

Une prise est validée avec 90 % de mots reconnus et un timing tenu à ±3 s. Trois prises validées débloquent le niveau suivant. La progression, la série et l'historique restent dans le navigateur.

## Format de `daily.json`

```json
{
  "date": "2026-10-23",
  "theme": "astronomie",
  "levels": {
    "1": {"titre": "…", "theme": "…", "texte": "…"},
    "2": {"titre": "…", "theme": "…", "texte": "…"}
  }
}
```
