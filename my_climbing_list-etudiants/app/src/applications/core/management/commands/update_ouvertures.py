from datetime import datetime
from django.core.management.base import BaseCommand
from applications.core.models import Ouverture, Salle
from applications.core.utils import fetch_csv_data, hold_colors, cotation_colors, EN_profil, EN_style, PT_cotations, PT_colors
import re


class Command(BaseCommand):
    help = "Met à jour ou crée de nouvelles ouvertures à partir d'un fichier CSV"

    def handle(self, *args, **kwargs):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("[%Y-%m-%d %H:%M:%S]")

        # Récupération des données CSV
        csv_data = fetch_csv_data("https://topo.example.test/topos.csv")

        if csv_data:
            self.bulk_update_or_create_ouvertures(csv_data, formatted_datetime)
        else:
            self.stdout.write(self.style.ERROR(f"{formatted_datetime} Échec de la récupération du fichier CSV"))

    def bulk_update_or_create_ouvertures(self, csv_data, formatted_datetime):
        # Récupération des données existantes en une seule requête
        ouvertures_existantes = {o.id: o for o in Ouverture.objects.all()}
        salles_existantes = {s.id: s for s in Salle.objects.all()}

        # Parsing et validation des données
        parsed_data = [self.parse_csv_row(row, salles_existantes, formatted_datetime) for row in csv_data]
        parsed_data = [data for data in parsed_data if data]  # Supprimer les lignes invalides

        # Séparation en mises à jour et créations
        ouvertures_a_creer, ouvertures_a_mettre_a_jour = self.process_bulk_updates(parsed_data, ouvertures_existantes)

        # Appliquer les opérations en masse
        self.apply_bulk_operations(ouvertures_a_creer, ouvertures_a_mettre_a_jour, formatted_datetime)

    def parse_csv_row(self, row, salles_existantes, formatted_datetime):
        """ Parse et formate une ligne du fichier CSV """
        try:
            ouverture_id = int(row[0])
            nom = row[1]
            date_ouverture = datetime.strptime(row[2], "%Y-%m-%d").date()
            salle_id = int(row[3])
            ouvreur = row[5]
            bloc = row[6] == "oui"
            relais = int(row[10])

            # Vérifier si la salle existe
            salle_obj = salles_existantes.get(salle_id)
            if not salle_obj:
                self.stdout.write(self.style.WARNING(f"{formatted_datetime} Salle {salle_id} non trouvée. Ignorée."))
                return None

            # Traitement des données PT vers FR
            if re.match(r"^[3-9]", row[8]):
                niveau = row[8]
            else:
                niveau = PT_cotations.get(row[8], "-")

            if row[11].lower() in ["conti", "rési", "bloc", "classic", "technic", "coordo", "tricky", "physic"]:
                style = row[11].lower()
            else:
                style = EN_style.get(row[11].lower(), "")

            if row[12].lower() in ["dalle", "dièdre", "vertical", "dévers", "gros dévers/toit", "gros dévers"]:
                profil = row[12].lower()
            else:
                profil = EN_profil.get(row[12].lower(), "")

            profil = "toit" if profil in ["gros dévers/toit", "gros dévers"] else profil

            # Couleur des prises
            couleur = row[7].split()[0] if row[7] else ""

            if couleur.lower() in hold_colors:
                pass  # on garde tel quel
            elif couleur.lower() in PT_colors:
                couleur = PT_colors[couleur.lower()]
            else:
                couleur = ""

            # Ignorer les entrées avec relais=0
            if relais == 0:
                return None

            # Déterminer la couleur HEX des prises
            hex_couleur = hold_colors.get(couleur, "#FFFFFF")

            # Déterminer la couleur HEX de la cotation
            niveau_couleur = cotation_colors.get(niveau[0], "#000000") if niveau else "#000000"

            return {
                "id": ouverture_id,
                "nom": nom,
                "date_ouverture": date_ouverture,
                "salle": salle_obj,
                "ouvreur": ouvreur,
                "bloc": bloc,
                "couleur": couleur,
                "hex_couleur": hex_couleur,
                "niveau": niveau,
                "niveau_couleur": niveau_couleur,
                "relais": relais,
                "profil": profil,
                "style": style,
                "active": True,
            }

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"{formatted_datetime} Erreur lors du parsing de la ligne: {row}"))
            self.stdout.write(self.style.ERROR(f"{formatted_datetime} {str(e)}"))
            return None

    @staticmethod
    def process_bulk_updates(parsed_data, ouvertures_existantes):
        """ Sépare les ouvertures à mettre à jour et celles à créer """
        ouvertures_a_creer = []
        ouvertures_a_mettre_a_jour = []

        for data in parsed_data:
            ouverture_id = data["id"]

            if ouverture_id in ouvertures_existantes:
                # Mise à jour d'une ouverture existante
                ouverture = ouvertures_existantes[ouverture_id]
                ouverture.nom = data["nom"]
                ouverture.date_ouverture = data["date_ouverture"]
                ouverture.salle = data["salle"]
                ouverture.ouvreur = data["ouvreur"]
                ouverture.bloc = data["bloc"]
                ouverture.couleur = data["couleur"]
                ouverture.hex_couleur = data["hex_couleur"]
                ouverture.niveau = data["niveau"]
                ouverture.niveau_couleur = data["niveau_couleur"]
                ouverture.relais = data["relais"]
                ouverture.profil = data["profil"]
                ouverture.style = data["style"]
                ouverture.active = True

                ouvertures_a_mettre_a_jour.append(ouverture)
            else:
                # Création d'une nouvelle ouverture
                ouvertures_a_creer.append(Ouverture(**data))

        return ouvertures_a_creer, ouvertures_a_mettre_a_jour

    def apply_bulk_operations(self, ouvertures_a_creer, ouvertures_a_mettre_a_jour, formatted_datetime):
        """ Applique les opérations de mise à jour et de création en masse """
        # Effectuer les mises à jour en une seule requête
        if ouvertures_a_mettre_a_jour:
            Ouverture.objects.bulk_update(
                ouvertures_a_mettre_a_jour,
                ["nom", "date_ouverture", "salle", "ouvreur", "bloc", "couleur", "hex_couleur",
                 "niveau", "niveau_couleur", "relais", "profil", "style", "active"]
            )
            self.stdout.write(self.style.SUCCESS(
                f"{formatted_datetime} {len(ouvertures_a_mettre_a_jour)} ouvertures mises à jour"
            ))

        # Effectuer les créations en une seule requête
        if ouvertures_a_creer:
            Ouverture.objects.bulk_create(ouvertures_a_creer)
            self.stdout.write(self.style.SUCCESS(
                f"{formatted_datetime} {len(ouvertures_a_creer)} nouvelles ouvertures ajoutées"
            ))
