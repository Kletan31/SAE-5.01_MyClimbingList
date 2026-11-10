<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20261109080619 extends AbstractMigration
{
    public function getDescription(): string
    {
        return 'Schéma V1 : salles, utilisateurs, ouvertures, séances, grimpes, suivis + gestion salles par staff';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('CREATE TABLE utilisateur_salle_geree (utilisateur_id INT NOT NULL, salle_id INT NOT NULL, INDEX IDX_8A0CE380FB88E14F (utilisateur_id), INDEX IDX_8A0CE380DC304035 (salle_id), PRIMARY KEY (utilisateur_id, salle_id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci`');
        $this->addSql('ALTER TABLE utilisateur_salle_geree ADD CONSTRAINT FK_8A0CE380FB88E14F FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id) ON DELETE CASCADE');
        $this->addSql('ALTER TABLE utilisateur_salle_geree ADD CONSTRAINT FK_8A0CE380DC304035 FOREIGN KEY (salle_id) REFERENCES salle (id) ON DELETE CASCADE');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE utilisateur_salle_geree DROP FOREIGN KEY FK_8A0CE380FB88E14F');
        $this->addSql('ALTER TABLE utilisateur_salle_geree DROP FOREIGN KEY FK_8A0CE380DC304035');
        $this->addSql('DROP TABLE utilisateur_salle_geree');
    }
}
