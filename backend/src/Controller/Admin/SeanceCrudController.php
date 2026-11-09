<?php

namespace App\Controller\Admin;

use App\Entity\Seance;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractCrudController;
use EasyCorp\Bundle\EasyAdminBundle\Field\AssociationField;
use EasyCorp\Bundle\EasyAdminBundle\Field\DateField;
use EasyCorp\Bundle\EasyAdminBundle\Field\DateTimeField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IdField;

/**
 * @extends AbstractCrudController<Seance>
 */
class SeanceCrudController extends AbstractCrudController
{
    public static function getEntityFqcn(): string
    {
        return Seance::class;
    }

    public function configureFields(string $pageName): iterable
    {
        return [
            IdField::new('id')->hideOnForm(),
            AssociationField::new('utilisateur'),
            AssociationField::new('salle'),
            DateField::new('dateSeance', 'Date'),
            AssociationField::new('grimpes', 'Grimpes')->hideOnForm(),
            DateTimeField::new('creeLe', 'Créée le')->onlyOnDetail(),
            DateTimeField::new('modifieLe', 'Modifiée le')->onlyOnDetail(),
        ];
    }
}
