<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20261109072323 extends AbstractMigration
{
    public function getDescription(): string
    {
        return 'Schéma V1 : salles, utilisateurs, ouvertures, séances, grimpes, suivis';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('CREATE TABLE grimpe (id INT AUTO_INCREMENT NOT NULL, montee INT DEFAULT 0 NOT NULL, top INT DEFAULT 0 NOT NULL, flash TINYINT DEFAULT 0 NOT NULL, montee_tete INT DEFAULT 0 NOT NULL, top_tete INT DEFAULT 0 NOT NULL, flash_tete TINYINT DEFAULT 0 NOT NULL, cree_le DATETIME NOT NULL, modifie_le DATETIME NOT NULL, seance_id INT NOT NULL, ouverture_id INT NOT NULL, UNIQUE INDEX UNIQ_GRIMPE_SEANCE_OUVERTURE (seance_id, ouverture_id), INDEX IDX_33E72135E3797A94 (seance_id), INDEX IDX_33E72135F892AC88 (ouverture_id), PRIMARY KEY (id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci`');
        $this->addSql('CREATE TABLE ouverture (id INT AUTO_INCREMENT NOT NULL, type VARCHAR(5) NOT NULL, cotation VARCHAR(50) NOT NULL, couleur VARCHAR(50) DEFAULT NULL, couleur_hex VARCHAR(11) DEFAULT NULL, date_creation DATE NOT NULL, relais INT DEFAULT NULL, secteur VARCHAR(100) DEFAULT NULL, statut VARCHAR(10) NOT NULL, date_demontage DATE DEFAULT NULL, en_tete TINYINT DEFAULT 0 NOT NULL, proprietes JSON DEFAULT NULL, salle_id INT NOT NULL, INDEX IDX_43461EABDC304035 (salle_id), PRIMARY KEY (id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci`');
        $this->addSql('CREATE TABLE salle (id INT AUTO_INCREMENT NOT NULL, nom VARCHAR(100) NOT NULL, ville VARCHAR(100) DEFAULT NULL, pays VARCHAR(2) DEFAULT NULL, masquer_cotations_recentes TINYINT DEFAULT 0 NOT NULL, image VARCHAR(255) DEFAULT NULL, PRIMARY KEY (id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci`');
        $this->addSql('CREATE TABLE seance (id INT AUTO_INCREMENT NOT NULL, date_seance DATE NOT NULL, cree_le DATETIME NOT NULL, modifie_le DATETIME NOT NULL, utilisateur_id INT NOT NULL, salle_id INT NOT NULL, UNIQUE INDEX UNIQ_SEANCE_UTILISATEUR_SALLE_DATE (utilisateur_id, salle_id, date_seance), INDEX IDX_DF7DFD0EFB88E14F (utilisateur_id), INDEX IDX_DF7DFD0EDC304035 (salle_id), PRIMARY KEY (id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci`');
        $this->addSql('CREATE TABLE suivi (id INT AUTO_INCREMENT NOT NULL, cree_le DATETIME NOT NULL, utilisateur_id INT NOT NULL, salle_id INT NOT NULL, UNIQUE INDEX UNIQ_SUIVI_UTILISATEUR_SALLE (utilisateur_id, salle_id), INDEX IDX_2EBCCA8FFB88E14F (utilisateur_id), INDEX IDX_2EBCCA8FDC304035 (salle_id), PRIMARY KEY (id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci`');
        $this->addSql('CREATE TABLE utilisateur (id INT AUTO_INCREMENT NOT NULL, email VARCHAR(180) NOT NULL, nom_utilisateur VARCHAR(50) NOT NULL, roles JSON NOT NULL, password VARCHAR(255) NOT NULL, nom VARCHAR(100) DEFAULT NULL, prenom VARCHAR(100) DEFAULT NULL, genre VARCHAR(1) DEFAULT NULL, langue VARCHAR(5) NOT NULL, date_inscription DATETIME NOT NULL, salle_favorite_id INT DEFAULT NULL, UNIQUE INDEX UNIQ_IDENTIFIER_EMAIL (email), UNIQUE INDEX UNIQ_UTILISATEUR_NOM_UTILISATEUR (nom_utilisateur), INDEX IDX_1D1C63B354A8DF9E (salle_favorite_id), PRIMARY KEY (id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci`');
        $this->addSql('ALTER TABLE grimpe ADD CONSTRAINT FK_33E72135E3797A94 FOREIGN KEY (seance_id) REFERENCES seance (id)');
        $this->addSql('ALTER TABLE grimpe ADD CONSTRAINT FK_33E72135F892AC88 FOREIGN KEY (ouverture_id) REFERENCES ouverture (id)');
        $this->addSql('ALTER TABLE ouverture ADD CONSTRAINT FK_43461EABDC304035 FOREIGN KEY (salle_id) REFERENCES salle (id)');
        $this->addSql('ALTER TABLE seance ADD CONSTRAINT FK_DF7DFD0EFB88E14F FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id)');
        $this->addSql('ALTER TABLE seance ADD CONSTRAINT FK_DF7DFD0EDC304035 FOREIGN KEY (salle_id) REFERENCES salle (id)');
        $this->addSql('ALTER TABLE suivi ADD CONSTRAINT FK_2EBCCA8FFB88E14F FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id)');
        $this->addSql('ALTER TABLE suivi ADD CONSTRAINT FK_2EBCCA8FDC304035 FOREIGN KEY (salle_id) REFERENCES salle (id)');
        $this->addSql('ALTER TABLE utilisateur ADD CONSTRAINT FK_1D1C63B354A8DF9E FOREIGN KEY (salle_favorite_id) REFERENCES salle (id) ON DELETE SET NULL');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE grimpe DROP FOREIGN KEY FK_33E72135E3797A94');
        $this->addSql('ALTER TABLE grimpe DROP FOREIGN KEY FK_33E72135F892AC88');
        $this->addSql('ALTER TABLE ouverture DROP FOREIGN KEY FK_43461EABDC304035');
        $this->addSql('ALTER TABLE seance DROP FOREIGN KEY FK_DF7DFD0EFB88E14F');
        $this->addSql('ALTER TABLE seance DROP FOREIGN KEY FK_DF7DFD0EDC304035');
        $this->addSql('ALTER TABLE suivi DROP FOREIGN KEY FK_2EBCCA8FFB88E14F');
        $this->addSql('ALTER TABLE suivi DROP FOREIGN KEY FK_2EBCCA8FDC304035');
        $this->addSql('ALTER TABLE utilisateur DROP FOREIGN KEY FK_1D1C63B354A8DF9E');
        $this->addSql('DROP TABLE grimpe');
        $this->addSql('DROP TABLE ouverture');
        $this->addSql('DROP TABLE salle');
        $this->addSql('DROP TABLE seance');
        $this->addSql('DROP TABLE suivi');
        $this->addSql('DROP TABLE utilisateur');
    }
}
