# Documentation administrateur – MyClimbingList
 
*Dernière mise à jour : 25/11/2026 – Version : 0.1*
 
Cette documentation s'adresse à la personne responsable de l'installation de MCL et de son bon fonctionnement.
 
## 1. Installation
 
### 1.1 Backend (API et backoffice)
 
#### Pré-requis
 
| Élément | Version |
|---|---|
| PHP | 8.4 (avec les extensions requises par Symfony et `pdo_mysql`) |
| Composer | 2.x |
| MySQL | 8.x |
| OpenSSL | Nécessaire pour générer les clés JWT |
| Symfony CLI | Optionnel, pour le serveur de développement |
 
#### Processus d'installation
 
1. Récupérer le code et se placer dans le dossier du backend :
```bash
git clone <URL_DU_DEPOT>
cd <DEPOT>/backend
```
2. Installer les dépendances :
```bash
composer install
```
3. Configurer l'environnement : copier `.env` vers `.env.local` et renseigner au minimum la connexion à la base
   (`DATABASE_URL`) et les paramètres JWT.
```
DATABASE_URL="mysql://UTILISATEUR:MOT_DE_PASSE@127.0.0.1:3306/NOM_BASE?serverVersion=8.0"
```
4. Générer les clés JWT :
```bash
php bin/console lexik:jwt:generate-keypair
```
5. Créer la base et appliquer les migrations (la base est entièrement reconstruite à partir des migrations) :
```bash
php bin/console doctrine:database:create
php bin/console doctrine:migrations:migrate
```
6. Créer le compte administrateur du backoffice :
```bash
php bin/console app:creer-admin
```
7. Démarrer le serveur :
```bash
symfony serve
```
   En production, configurer un serveur web (Apache ou Nginx) pointant vers `back/public/`.
 
#### Vérifier que l'installation est réussie
 
| Vérification | Résultat attendu |
|---|---|
| `GET /api/salles` | Code 200 et un tableau JSON |
| Page `/admin` | Page de connexion du backoffice, connexion possible avec le compte créé à l'étape 6 |
| `php bin/phpunit` | Tests au vert (voir le [cahier de recette](./cahier-de-recette.md)) |
 
### 1.2 Application mobile (Flutter)
 
> **À compléter (Front)**
 
#### Pré-requis
 
> Version de Flutter, SDK Android / Xcode, etc.
 
#### Processus d'installation et de build
 
> Installation des dépendances, configuration de l'URL de l'API, build Android et iOS.
 
#### Publication sur les stores
 
> Étapes de publication (comptes développeur, signature, soumission).
 
#### Vérifier que l'installation est réussie
 
> Comment s'assurer que l'application se connecte bien à l'API.
 
## 2. Bon fonctionnement
 
### 2.1 Rôle de l'administrateur
 
| Rôle | Responsabilités |
|---|---|
| Administrateur | Installer et mettre à jour l'application, créer les comptes du backoffice, surveiller le bon fonctionnement |
| Direction | Accès à l'ensemble des données depuis le backoffice |
| Staff | Accès à sa salle et aux séances des utilisateurs ayant autorisé sa salle |
 
> Le périmètre exact du staff et de la direction est en attente de validation par le client.
 
### 2.2 Utilisation du backoffice
 
Le backoffice (EasyAdmin) est accessible sous `/admin`. Il permet de gérer :
 
| Section | Actions |
|---|---|
| Salles | Consulter, créer, modifier |
| Ouvertures | Consulter, créer, modifier |
| Utilisateurs | Consulter, modifier |
| Séances, grimpes, suivis | À venir (extension prévue du backoffice) |
 
> À compléter : captures d'écran et procédures courantes (créer un compte staff, rattacher un staff à une salle).
 
### 2.3 Mises à jour
 
1. Récupérer la nouvelle version du code (`git pull` ou nouvelle release).
2. Mettre à jour les dépendances : `composer install`.
3. Appliquer les nouvelles migrations : `php bin/console doctrine:migrations:migrate`.
4. Vider le cache : `php bin/console cache:clear`.
> À compléter : procédure de mise à jour de l'application mobile (**Front**).
 
### 2.4 Sauvegardes
 
> À compléter : fréquence et méthode de sauvegarde de la base MySQL, et procédure de restauration.
 
### 2.5 Surveillance
 
> À compléter : journaux à consulter (`back/var/log/`), indicateurs à surveiller.
 
## 3. En cas de panne
 
| Symptôme | Cause probable | Action |
|---|---|---|
| L'API répond 401 pour tous les utilisateurs | Clés JWT absentes ou modifiées, jetons expirés | Vérifier la présence des clés, régénérer si besoin (les utilisateurs devront se reconnecter) |
| L'API répond 500 | Erreur applicative ou base inaccessible | Consulter `back/var/log/`, vérifier la connexion à la base |
| Erreur de connexion à la base | `DATABASE_URL` incorrecte ou MySQL arrêté | Vérifier la configuration et l'état du service MySQL |
| Tables ou colonnes manquantes | Migrations non appliquées | Lancer `php bin/console doctrine:migrations:migrate` |
| Connexion au backoffice impossible | Compte administrateur absent | Recréer le compte avec `php bin/console app:creer-admin` |
| *Symptôme côté application mobile* | | **À compléter (Front)** |
 
> À compléter : contacts de l'équipe et du client (Altissimo) en cas d'incident.
 
