<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20261021223954 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('CREATE TABLE ouverture (id INT AUTO_INCREMENT NOT NULL, discipline VARCHAR(5) NOT NULL, relais INT NOT NULL, cotation VARCHAR(50) NOT NULL, couleur VARCHAR(50) DEFAULT NULL, couleur_hex VARCHAR(11) DEFAULT NULL, date_ouverture DATE NOT NULL, statut VARCHAR(10) NOT NULL, date_demontage DATE DEFAULT NULL, salle_id INT NOT NULL, INDEX IDX_43461EABDC304035 (salle_id), PRIMARY KEY (id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci`');
        $this->addSql('CREATE TABLE salle (id INT AUTO_INCREMENT NOT NULL, nom VARCHAR(100) NOT NULL, ville VARCHAR(100) DEFAULT NULL, pays VARCHAR(2) DEFAULT NULL, masquer_cotations_recentes TINYINT NOT NULL, PRIMARY KEY (id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci`');
        $this->addSql('CREATE TABLE utilisateur (id INT AUTO_INCREMENT NOT NULL, email VARCHAR(180) NOT NULL, roles JSON NOT NULL, password VARCHAR(255) NOT NULL, nom VARCHAR(100) DEFAULT NULL, prenom VARCHAR(100) DEFAULT NULL, genre VARCHAR(1) DEFAULT NULL, langue VARCHAR(5) NOT NULL, date_inscription DATETIME NOT NULL, salle_favorite_id INT DEFAULT NULL, UNIQUE INDEX UNIQ_IDENTIFIER_EMAIL (email), INDEX IDX_1D1C63B354A8DF9E (salle_favorite_id), PRIMARY KEY (id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci`');
        $this->addSql('ALTER TABLE ouverture ADD CONSTRAINT FK_43461EABDC304035 FOREIGN KEY (salle_id) REFERENCES salle (id)');
        $this->addSql('ALTER TABLE utilisateur ADD CONSTRAINT FK_1D1C63B354A8DF9E FOREIGN KEY (salle_favorite_id) REFERENCES salle (id)');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE ouverture DROP FOREIGN KEY FK_43461EABDC304035');
        $this->addSql('ALTER TABLE utilisateur DROP FOREIGN KEY FK_1D1C63B354A8DF9E');
        $this->addSql('DROP TABLE ouverture');
        $this->addSql('DROP TABLE salle');
        $this->addSql('DROP TABLE utilisateur');
    }
}
