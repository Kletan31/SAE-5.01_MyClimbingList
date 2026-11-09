<?php

namespace App\Controller\Admin;

use App\Entity\Grimpe;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractCrudController;
use EasyCorp\Bundle\EasyAdminBundle\Field\AssociationField;
use EasyCorp\Bundle\EasyAdminBundle\Field\BooleanField;
use EasyCorp\Bundle\EasyAdminBundle\Field\DateTimeField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IdField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IntegerField;

/**
 * @extends AbstractCrudController<Grimpe>
 */
class GrimpeCrudController extends AbstractCrudController
{
    public static function getEntityFqcn(): string
    {
        return Grimpe::class;
    }

    public function configureFields(string $pageName): iterable
    {
        return [
            IdField::new('id')->hideOnForm(),
            AssociationField::new('seance', 'Séance'),
            AssociationField::new('ouverture', 'Ouverture'),
            IntegerField::new('montee', 'Montées'),
            IntegerField::new('top', 'Tops'),
            BooleanField::new('flash', 'Flash'),
            IntegerField::new('monteeTete', 'Montées (tête)')->hideOnIndex(),
            IntegerField::new('topTete', 'Tops (tête)')->hideOnIndex(),
            BooleanField::new('flashTete', 'Flash (tête)')->hideOnIndex(),
            DateTimeField::new('creeLe', 'Créée le')->onlyOnDetail(),
            DateTimeField::new('modifieLe', 'Modifiée le')->onlyOnDetail(),
        ];
    }
}
