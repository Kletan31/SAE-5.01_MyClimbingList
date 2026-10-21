<?php

namespace App\Controller\Admin;

use App\Entity\Ouverture;
use EasyCorp\Bundle\EasyAdminBundle\Config\Action;
use EasyCorp\Bundle\EasyAdminBundle\Config\Actions;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractCrudController;
use EasyCorp\Bundle\EasyAdminBundle\Field\AssociationField;
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
            ChoiceField::new('discipline')->setChoices(['Voie' => 'voie', 'Bloc' => 'bloc']),
            IntegerField::new('relais'),
            TextField::new('cotation'),
            TextField::new('couleur'),
            TextField::new('couleur_hex', 'Couleur (hex)'),
            DateField::new('date_ouverture', "Date d'ouverture"),
            ChoiceField::new('statut')->setChoices(['Actif' => 'actif', 'Démonté' => 'demonte']),
            DateField::new('date_demontage', 'Date de démontage'),
        ];
    }
}