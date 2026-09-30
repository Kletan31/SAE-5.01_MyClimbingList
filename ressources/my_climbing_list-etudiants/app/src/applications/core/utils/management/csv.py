import csv
import requests
import chardet


def fetch_csv_data(url):
    from django.core.management.base import CommandError
    raise CommandError("Import distant désactivé dans le livrable étudiant ; utiliser seed_demo.")
    response = requests.get(url)

    if response.status_code != 200:
        return None

    # Détection de l'encodage
    raw_data = response.content
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    response.encoding = encoding

    # Lecture du fichier CSV avec l'encodage détecté
    csv_data = csv.reader(response.text.splitlines(), delimiter=',')
    next(csv_data)  # Saut de l'en-tête
    return csv_data
