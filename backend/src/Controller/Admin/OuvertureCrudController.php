<?php

namespace App\Controller\Admin;

use App\Entity\Ouverture;
use EasyCorp\Bundle\EasyAdminBundle\Config\Action;
use EasyCorp\Bundle\EasyAdminBundle\Config\Actions;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractCrudController;
use EasyCorp\Bundle\EasyAdminBundle\Field\AssociationField;
use EasyCorp\Bundle\EasyAdminBundle\Field\BooleanField;
use EasyCorp\Bundle\EasyAdminBundle\Field\ChoiceField;
use EasyCorp\Bundle\EasyAdminBundle\Field\DateField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IdField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IntegerField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TextField;

/**
 * @extends AbstractCrudController<Ouverture>
 */
class OuvertureCrudController extends AbstractCrudController
{
    public static function getEntityFqcn(): string
    {
        return Ouverture::class;
    }

    public function configureActions(Actions $actions): Actions
    {
        // Une ouverture n'est jamais supprimée : on la passe au statut "démonté".
        return $actions->disable(Action::DELETE);
    }

    public function configureFields(string $pageName): iterable
    {
        return [
            IdField::new('id')->hideOnForm(),
            AssociationField::new('salle'),
            // Champs liés à un enum PHP : EasyAdmin détecte l'enum et propose ses cas
            ChoiceField::new('type'),
            TextField::new('cotation'),
            TextField::new('couleur')->hideOnIndex(),
            TextField::new('couleurHex', 'Couleur (hex)')->hideOnIndex(),
            IntegerField::new('relais')->hideOnIndex(),
            TextField::new('secteur')->hideOnIndex(),
            BooleanField::new('enTete', 'Faisable en tête')
                ->setHelp('Ignoré pour un bloc (toujours non).'),
            ChoiceField::new('statut'),
            DateField::new('dateCreation', "Date d'ouverture"),
            DateField::new('dateDemontage', 'Date de démontage')->hideOnIndex(),
            // "proprietes" volontairement absent (champ provisoire)
        ];
    }
}
