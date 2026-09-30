# My Climbing List — Flutter POC

Initialisation volontairement légère du projet mobile, basée sur la première version du cahier des charges.

## Objectif
Ce dépôt sert uniquement de POC / socle d'initialisation en attendant les retours du client. Il ne contient ni backend, ni authentification réelle, ni données métier réelles.

## Écrans prototypes
- Accueil
- Topo
- Nouvelle séance
- Projets
- Profil

La navigation principale est déjà structurée. Les contenus sont des placeholders afin d'éviter de figer trop tôt les choix fonctionnels et graphiques.

## Suite proposée
1. Valider avec le client l'arborescence et les écrans.
2. Définir les parcours prioritaires.
3. Mettre en place l'architecture API / modèles.
4. Ajouter l'authentification et le stockage local.
5. Implémenter progressivement les fonctionnalités du cahier des charges.

## Lancer
Avec Flutter installé :

```bash
flutter pub get
flutter run
```

Le projet vise une base Flutter récente compatible Android/iOS. La contrainte du cahier des charges concernant Android 7+ devra être vérifiée et figée lors de la configuration finale du SDK et des plugins.
