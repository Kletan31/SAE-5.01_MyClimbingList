# My Climbing List

## À propos

My Climbing List (MCL) est un POC développé pour Altissimo. Il permet aux grimpeurs de consulter les ouvertures et d’enregistrer leurs pratiques ; le code contient aussi des usages staff, direction et compétition.

Ce dépôt est une **copie étudiante assainie**, destinée à l’étude et à la reprise technique. Ce n’est pas une copie exploitable de la production.

## Démarrage rapide

Installez et démarrez [Docker](https://docs.docker.com/get-started/get-docker/), puis installez [mkcert](https://github.com/FiloSottile/mkcert#installation). Depuis la racine du dépôt :

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

**Puis, sur les trois plateformes** : installez la confiance locale et générez les certificats au premier démarrage de cette machine.

```text
mkcert -install
mkcert -cert-file .local/certs/localhost.pem -key-file .local/certs/localhost-key.pem localhost 127.0.0.1 "::1"
docker compose -p mcl-local -f docker-compose.local.yml up --build
```

Ouvrez **https://localhost:8443** lorsque les services sont prêts. Gardez le terminal ouvert.

## Compte de démonstration

- Utilisateur : `demo.climb`
- Mot de passe : `demo-mcl`

## Documentation

- [Démarrage local : étapes, arrêt, reset et dépannage](docs/etudiants/MCL_DEMARRAGE_LOCAL.md)
- [Ordre de lecture étudiant](docs/etudiants/README.md)
- [Références techniques](docs/reference/)
- [Périmètre de l’assainissement](docs/ASSAINISSEMENT.md)

## Important

La démo utilise uniquement des données synthétiques ; aucun accès à la production n’est nécessaire. N’ajoutez jamais de secrets au dépôt : `.env` et `.local/`, notamment les certificats et clés, doivent rester ignorés par Git.
