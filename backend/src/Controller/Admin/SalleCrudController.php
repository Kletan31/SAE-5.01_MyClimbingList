<?php

namespace App\Controller\Admin;

use App\Entity\Salle;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractCrudController;
use EasyCorp\Bundle\EasyAdminBundle\Field\BooleanField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IdField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TextField;

/**
 * @extends AbstractCrudController<Salle>
 */
class SalleCrudController extends AbstractCrudController
{
    public static function getEntityFqcn(): string
    {
        return Salle::class;
    }

    public function configureFields(string $pageName): iterable
    {
        return [
            IdField::new('id')->hideOnForm(),
            TextField::new('nom'),
            TextField::new('ville'),
            TextField::new('pays', 'Pays (code à 2 lettres)'),
            BooleanField::new('masquerCotationsRecentes', 'Masquer les cotations récentes'),
            // Stockage des images à clarifier : champ texte (nom de fichier ou URL) en attendant
            TextField::new('image', 'Image (nom ou URL)')->hideOnIndex(),
        ];
    }
}
