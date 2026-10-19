| Méthode | Route | Accès | But | Réponses |
|----------|--------|--------|-----|-----------|
| POST | `/auth/register` | Public | Créer un compte | `201` / `409` / `422` |
| POST | `/auth/login` | Public | Connexion, émission des jetons | `200` / `401` / `429` |
| POST | `/auth/refresh` | Refresh token | Renouveler le jeton d’accès | `200` / `401` |
| POST | `/auth/password-reset` | Public | Demander une réinitialisation | `202` |
| GET | `/me` | JWT | Lire son profil | `200` / `401` |
| PATCH | `/me` | JWT | Modifier son profil | `200` / `401` / `422` |
| DELETE | `/me` | JWT | Supprimer son compte et traiter ses données | `204` / `401` |
| GET | `/salles` | Public ou JWT | Lister les salles | `200` |
| GET | `/salles/{salleId}` | Public ou JWT | Détail d’une salle | `200` / `404` |
| PUT | `/salles/{salleId}/favorite` | JWT | Définir sa salle favorite | `204` / `404` |
| DELETE | `/salles/{salleId}/favorite` | JWT | Retirer sa salle favorite | `204` / `404` |
| GET | `/salles/{salleId}/ouvertures` | Public ou JWT | Topo avec filtres et pagination | `200` / `404` |
| GET | `/ouvertures/{ouvertureId}` | Public ou JWT | Détail d’une ouverture | `200` / `404` |
| GET | `/seances` | JWT | Lister ses séances ; filtres `from/to`, pagination | `200` / `401` |
| POST | `/seances` | JWT | Créer une séance et ses lignes en une transaction | `201` / `409` / `422` |
| GET | `/seances/{seanceId}` | JWT | Détail d’une séance personnelle | `200` / `404` |
| PUT | `/seances/{seanceId}` | JWT | Remplacer une séance et ses lignes | `200` / `404` / `409` / `422` |
| DELETE | `/seances/{seanceId}` | JWT | Supprimer une séance et ses lignes | `204` / `404` |
| GET | `/carnet` | JWT | Palmarès agrégé par ouverture, avec filtres | `200` / `401` |

Méthodes :
- GET : Lire / récupérer une ressource.
- POST : Créer une ressource ou déclencher une action.
- PATCH : Modifier partiellement une ressource.
- PUT : Remplacer entièrement une ressource ou définir un état.
- DELETE : Supprimer une ressource.

Codes :
- 200 OK
- 201 Created : Ressource créée avec succès.
- 202 Accepted : Action acceptée mais traitée plus tard.
- 204 No Content : Succès, mais aucune donnée.
- 401 Unauthorized : Jeton manquant ou invalide.
- 404 Not Found : Ressource inexistante.
- 409 Conflict : Conflit logique (doublon).
- 422 Unprocessable Entity : Données invalides ou format incorrect.
- 429 Too Many Requests : Rate limit atteint.
