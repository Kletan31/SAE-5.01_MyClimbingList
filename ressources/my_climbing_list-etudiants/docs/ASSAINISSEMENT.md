# Copie étudiante MCL

Cette copie conserve le POC et sa démo fictive. La source historique reste séparée et inchangée. Aucun historique Git de production n’est repris.

- Démarrage : `docker compose -p mcl-local -f docker-compose.local.yml up --build -d` après copie de `.env.example` vers `.env` et génération mkcert de `.local/certs/localhost.pem` et `.local/certs/localhost-key.pem` pour localhost, 127.0.0.1 et ::1.
- URL : https://localhost:8443 ; comptes `demo.climb`, `demo.climb2`, mot de passe fictif `demo-mcl`.
- Le volume `mcl-local_postgres_local` est propre au projet Compose `mcl-local`. Un autre nom de projet utilise un volume distinct ; un reset `down --volumes` efface uniquement la base du projet concerné.
- 104 migrations historiques exclues : 57 structurelles et 47 avec traitements de données, dont comptes et historique individuel. Les modèles sont conservés ; migrations Django natives puis `--run-syncdb` pour les apps désactivées dans `MIGRATION_MODULES`. Aucun nouvel arbre de migrations.
- Configuration historique conservée pour lecture, assainie et bloquée à l’exécution. Seul `config.settings_local` est utilisable. Imports distants désactivés, contacts remplacés par `example.test`.
- Exclus : environnements historiques, TLS/ACME, Certbot, scripts de déploiement, logs, IDE, node_modules, photos/captures/plans réels. Plans de démo synthétiques conservés.
- Font Awesome Pro exclu ; Free 6.6.0 (paquet officiel @fortawesome/fontawesome-free) inclus avec LICENSE.txt. Quelques pictogrammes Pro sont remplacés par des équivalents Free.
- SVG de démonstration : dimensions explicites ajoutées pour le zoom historique ; version du cache local distincte. Pour un navigateur ayant utilisé la source, ouvrir une session privée ou effacer les données de localhost.
- Les rapports de référence décrivent l’ancienne source : leurs chemins exclus et procédures historiques ne constituent pas des instructions de lancement étudiant.
- Distribuer les fichiers du commit Git, jamais une archive brute du dossier de travail : `.env` et `.local/` servent uniquement aux tests sur cette machine.

Le [guide de démarrage étudiant](etudiants/MCL_DEMARRAGE_LOCAL.md) décrit la procédure locale. Staff/Elo/Direction/Contest ne sont pas des démonstrations complètes.
