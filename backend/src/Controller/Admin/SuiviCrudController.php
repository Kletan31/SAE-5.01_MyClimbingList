<?php

namespace App\Controller\Admin;

use App\Entity\Suivi;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractCrudController;
use EasyCorp\Bundle\EasyAdminBundle\Field\AssociationField;
use EasyCorp\Bundle\EasyAdminBundle\Field\DateTimeField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IdField;

/**
 * @extends AbstractCrudController<Suivi>
 */
class SuiviCrudController extends AbstractCrudController
{
    public static function getEntityFqcn(): string
    {
        return Suivi::class;
    }

    public function configureFields(string $pageName): iterable
    {
        return [
            IdField::new('id')->hideOnForm(),
            AssociationField::new('utilisateur', 'Utilisateur suivi'),
            AssociationField::new('salle', 'Salle autorisée'),
            DateTimeField::new('creeLe', 'Autorisé le')->hideOnForm(),
        ];
    }
}
