# Repères provisoires — démo fictive

- URL : https://localhost:8443
- Comptes : `demo.climb` (principal), `demo.climb2` ; mot de passe local `demo-mcl`.
- Emails : mêmes identifiants sous `example.test`.
- 3 salles : Démo Voie (9001), Démo Bloc (9002), Démo Mixte (9003).
- 18 ouvertures ; 15 pratiques pour le compte principal, 4 pour le second.
- Les pratiques sont agrégées par utilisateur/ouverture/date, pas par tentative.
- Dates relatives au premier seed ; option `seed_demo --reference-date YYYY-MM-DD`
  sur une base non initialisée pour fixer la référence.

## Parcours vérifiés le 12 septembre 2026

Connexion, accueil, sélection des salles, topo voie et bloc avec plans SVG fictifs,
carnet (dont ouverture inactive), filtres flash/tête et projets.
- Patience orange : essais sans top, projet classique.
- Cap vers la tête : top moulinette, pas de top tête, reste projet.
- Sommet acquis : top tête, absent des projets.
- Équilibre à trouver : projet bloc.
- Souvenir démonté : inactive, toujours dans le carnet.

Écriture réelle dans Chrome : 2 essais sans top sur Patience orange à la date
courante ; visible après redémarrage de web. Un nouveau `up` et un nouveau seed
conservent cette écriture. Le reset testé ensuite a supprimé cette écriture
comme prévu et recréé uniquement les 19 pratiques initiales.

## Initialisation / reset

`init` prépare le schéma puis appelle `seed_demo`. Le groupe sans droits
`mcl-local-demo-v1` sert de marqueur transactionnel. S'il existe, le seed ne
modifie rien, même si un étudiant a supprimé ou modifié des éléments.
Une collision d'IDs/comptes sans marqueur provoque un refus sans écrasement.

Reset destructif limité au bac à sable (certificats mkcert conservés) :

```sh
docker compose -p mcl-local -f docker-compose.local.yml down --volumes
docker compose -p mcl-local -f docker-compose.local.yml up --build
```

Après reset, se déconnecter/reconnecter dans le navigateur pour vider le cache
PWA de l'ancien état. Le service worker historique conserve des pages en cache.

Test HTTPS reproductible depuis la racine, avec Python 3 et le certificat PUBLIC
`rootCA.pem` de mkcert :

```sh
python3 scripts/check_demo_https.py --ca "/chemin/vers/rootCA.pem"
```

Ces tests lisent les pages rendues et vérifient les projets et ressources locales ;
ils ne pilotent pas les clics navigateur. Les clics et la saisie ont été testés
séparément dans Chrome. `demo.climb2` est créé mais son parcours n'a pas été testé.

## Non préparé

Staff, progression/Elo, direction et compétition : volontairement reportés pour
respecter le budget. Aucun traitement Elo ou réseau n'est lancé par le seed.
Pas de validation exhaustive des autres fonctionnalités du POC.
