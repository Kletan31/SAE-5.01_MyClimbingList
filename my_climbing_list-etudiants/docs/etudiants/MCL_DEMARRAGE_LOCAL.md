# Démarrer My Climbing List en local

Ce guide concerne le livrable étudiant et son environnement Docker local. Toutes les commandes se lancent **depuis la racine du dépôt**, là où se trouve `docker-compose.local.yml`.

## 1. Prérequis

- [Docker Desktop](https://docs.docker.com/get-started/get-docker/) ou Docker Engine avec le plugin Compose, installé et démarré. Sous Windows, utiliser les conteneurs Linux.
- [mkcert](https://github.com/FiloSottile/mkcert#installation), installé sur la machine où vous ouvrez le navigateur.
- Un navigateur moderne.

Le premier build nécessite Internet pour télécharger les images et dépendances. Il ne contacte pas la production MCL. Python et PostgreSQL sont fournis par les conteneurs : inutile de les installer sur votre machine.

## 2. Préparer l’environnement

**macOS / Linux**

```bash
test -f .env || cp .env.example .env
mkdir -p .local/certs
```

**Windows PowerShell**

```powershell
if (!(Test-Path .env)) { Copy-Item .env.example .env }
New-Item -ItemType Directory -Force .local/certs | Out-Null
```

Ces commandes préservent un `.env` existant. Pour ce parcours, gardez les valeurs locales fournies par `.env.example` et le nom de projet `mcl-local` dans les commandes Compose.

## 3. Générer le certificat HTTPS

Au premier démarrage sur chaque machine, exécutez ces deux commandes, identiques en shell macOS/Linux et en PowerShell :

```text
mkcert -install
mkcert -cert-file .local/certs/localhost.pem -key-file .local/certs/localhost-key.pem localhost 127.0.0.1 "::1"
```

`mkcert -install` installe une autorité de certification locale dans les magasins de confiance pris en charge. La seconde commande crée le certificat et sa clé aux chemins attendus par Compose et nginx, pour `localhost`, `127.0.0.1` et `::1`. Une demande de droits administrateur peut apparaître.

Ne commitez jamais ces fichiers : `.local/certs/` est ignoré. Ne partagez pas non plus la clé de l’autorité mkcert. Vous n’avez pas à régénérer les certificats à chaque lancement ni après un reset de la base.

Avec Firefox, la confiance peut nécessiter une configuration supplémentaire selon la plateforme ; voir la [documentation mkcert](https://github.com/FiloSottile/mkcert#supported-root-stores).

## 4. Lancer MCL

```bash
docker compose -p mcl-local -f docker-compose.local.yml up --build
```

Compose démarre PostgreSQL (`db`), puis l’initialisation du schéma et du seed (`init`), Django (`web`) et nginx HTTPS (`proxy`). Le service `init` qui termine avec le code `0` est normal : il a fini son travail.

Attendez le démarrage de `web` et `proxy`, puis gardez ce terminal ouvert. Le premier build peut prendre plusieurs minutes. Pour lancer en arrière-plan, ajoutez `-d` à la commande.

## 5. Ouvrir l’application

Ouvrez **https://localhost:8443** et connectez-vous avec :

- Utilisateur : `demo.climb`
- Mot de passe : `demo-mcl`

Le deuxième compte fictif, `demo.climb2`, utilise le même mot de passe. Le parcours de référence est celui de `demo.climb`.

## 6. Ce qu’il faut explorer

1. Depuis le bouton `+`, choisissez **Démo Voie** et consultez les ouvertures en liste ou sur le plan.
2. Consultez **Démo Bloc** et comparez les cotations et les pratiques.
3. Consultez les séances depuis l’accueil, puis ouvrez votre profil (icône en haut à droite) et **Mon Carnet**, en voie ou en bloc.
4. Ouvrez **Projets** pour observer les ouvertures encore en projet.
5. Sélectionnez une ouverture dans le topo, renseignez une pratique et validez son enregistrement.
6. Dans un deuxième terminal, depuis la racine du dépôt, redémarrez Django :

```bash
docker compose -p mcl-local -f docker-compose.local.yml restart web
```

Attendez quelques secondes, rechargez l’application et retrouvez votre pratique dans l’historique. Un redémarrage ne réinitialise pas la base.

## 7. Démo disponible

La base initiale contient **3 salles** — Démo Voie, Démo Bloc et Démo Mixte —, **18 ouvertures**, 2 comptes et 19 pratiques synthétiques. Elle illustre essais, tops, flash, moulinette, tête, projets et historique, avec une ouverture inactive et des plans SVG fictifs.

Toutes les données de cette démo sont fictives : aucune vraie salle ni aucun vrai grimpeur. Les modifications sont conservées aux lancements suivants ; le seed ne les écrase pas.

## 8. Arrêter l’environnement

Si Compose occupe le terminal, utilisez `Ctrl+C` pour arrêter les services, puis :

```bash
docker compose -p mcl-local -f docker-compose.local.yml down
```

Cette commande retire les conteneurs et réseaux du projet, mais conserve les données PostgreSQL et vos certificats.

## 9. Redémarrer sans perdre les données

```bash
docker compose -p mcl-local -f docker-compose.local.yml up --build
```

PostgreSQL retrouve ses données dans le volume Docker `mcl-local_postgres_local`. Compose préfixe le volume par le nom du projet ; gardez le même `-p` pour le lancement, l’arrêt et le reset. Vous retrouvez les pratiques enregistrées tant que ce volume n’a pas été supprimé.

## 10. Remettre la démo à zéro

**Cette opération efface toutes vos modifications dans la base étudiante.** Arrêtez la commande Compose au premier plan si nécessaire, puis exécutez :

```bash
docker compose -p mcl-local -f docker-compose.local.yml down --volumes
docker compose -p mcl-local -f docker-compose.local.yml up --build
```

Le volume DB est supprimé ; l’initialisation recrée le schéma et réinjecte la démo synthétique. `.env`, les certificats dans `.local/certs/` et l’autorité mkcert restent en place. Reconnectez-vous après le reset.

## 11. Problèmes fréquents

| Symptôme | Solution |
|---|---|
| `Cannot connect to the Docker daemon` | Démarrez Docker Desktop ou le service Docker, puis relancez Compose. |
| `mkcert` introuvable | Installez mkcert selon sa documentation officielle, puis rouvrez le terminal. |
| Compose signale une variable requise manquante | Vérifiez que vous êtes à la racine et préparez `.env` comme à l’étape 2. Comparez un fichier existant à `.env.example` sans l’écraser aveuglément. |
| Fichier de certificat absent / erreur de montage | Vérifiez les deux fichiers `.local/certs/localhost.pem` et `localhost-key.pem`, puis effectuez l’étape 3 s’ils manquent. |
| Port `8443` déjà utilisé | Arrêtez l’autre service local qui occupe ce port, puis relancez Compose. |
| Certificat non approuvé, notamment dans Firefox | Exécutez `mkcert -install` sur la machine du navigateur et redémarrez-le. Pour Firefox, suivez la configuration de confiance indiquée par mkcert ; ne contournez pas l’alerte. |
| Ancienne interface, plan invisible ou PWA obsolète | Essayez une fenêtre privée ; si elle fonctionne, effacez les données du site `localhost:8443` dans le navigateur puis reconnectez-vous. |
| Session incohérente après un reset | Rechargez la page de connexion ; si nécessaire, effacez les données du site puis reconnectez-vous avec le compte de démo. |

Pour voir l’état des services et les derniers messages, depuis un autre terminal :

```bash
docker compose -p mcl-local -f docker-compose.local.yml ps -a
docker compose -p mcl-local -f docker-compose.local.yml logs --tail=50 init web proxy
```

## 12. Ce que cette démo ne couvre pas

- Staff et Direction : pas de parcours de démonstration préparé.
- Elo/progression : calculs non exécutés automatiquement au démarrage.
- Contest : pas de démonstration complète préparée.
- Aucune connexion à la production, aucun import de données réelles.

Ces fonctionnalités peuvent exister dans le code sans être prêtes à explorer avec les comptes de démo.

## 13. Architecture locale

```text
Navigateur
    |
https://localhost:8443
    |
nginx (proxy)
    | HTTP réseau Docker interne
Django (web:8000)
    |
PostgreSQL 16 (db / mcl_demo)
```

Seul nginx est publié sur la boucle locale de votre machine ; Django et PostgreSQL restent sur le réseau Docker interne. Django utilise `config.settings_local`.

## 14. Où continuer

Consultez ensuite, selon votre besoin :

- [Analyse technique](../reference/MCL_ANALYSE_TECHNIQUE.md) : architecture et fonctionnement du code.
- [Notice de reprise](../reference/MCL_NOTICE_REPRISE.md) : périmètre et points de vigilance.
- [Recommandations de refonte](../reference/MCL_RECOMMANDATIONS_REFONTE.md) : pistes pour une éventuelle reprise.
- [Notes d’assainissement](../ASSAINISSEMENT.md) et [validation du livrable](../VALIDATION_PASSATION.md).

Les rapports de référence décrivent aussi le projet historique et peuvent citer des fichiers exclus. Pour lancer le livrable, suivez le présent guide. Poursuivez avec [Comprendre My Climbing List](MCL_COMPRENDRE.md) ; l’[index étudiant](README.md) présente l’ordre de lecture.
