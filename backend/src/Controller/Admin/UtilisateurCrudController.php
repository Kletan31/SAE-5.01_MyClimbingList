<?php

namespace App\Controller\Admin;

use App\Entity\Utilisateur;
use Doctrine\ORM\EntityManagerInterface;
use EasyCorp\Bundle\EasyAdminBundle\Config\Crud;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractCrudController;
use EasyCorp\Bundle\EasyAdminBundle\Field\AssociationField;
use EasyCorp\Bundle\EasyAdminBundle\Field\ChoiceField;
use EasyCorp\Bundle\EasyAdminBundle\Field\DateTimeField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IdField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TextField;
use Symfony\Component\Form\Extension\Core\Type\PasswordType;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

/**
 * @extends AbstractCrudController<Utilisateur>
 */
class UtilisateurCrudController extends AbstractCrudController
{
    public function __construct(private UserPasswordHasherInterface $passwordHasher)
    {
    }

    public static function getEntityFqcn(): string
    {
        return Utilisateur::class;
    }

    public function configureFields(string $pageName): iterable
    {
        return [
            IdField::new('id')->hideOnForm(),
            TextField::new('nomUtilisateur', "Nom d'utilisateur"),
            TextField::new('email'),
            TextField::new('nom')->hideOnIndex(),
            TextField::new('prenom', 'Prénom')->hideOnIndex(),
            TextField::new('genre')->hideOnIndex(),
            TextField::new('langue'),
            AssociationField::new('salleFavorite', 'Salle favorite')->hideOnIndex(),
            TextField::new('plainPassword', 'Mot de passe')
                ->setFormType(PasswordType::class)
                ->setRequired($pageName === Crud::PAGE_NEW)
                ->setHelp($pageName === Crud::PAGE_EDIT ? 'Laisser vide pour ne pas changer le mot de passe.' : '')
                ->onlyOnForms(),
            ChoiceField::new('roles')
                ->setChoices([
                    'Utilisateur' => 'ROLE_USER',
                    'Staff' => 'ROLE_STAFF',
                    'Direction' => 'ROLE_DIRECTION',
                ])
                ->allowMultipleChoices()
                ->renderExpanded(),
            DateTimeField::new('dateInscription', "Date d'inscription")->hideOnForm(),
            AssociationField::new('sallesGerees', 'Salles gérées (staff)')->hideOnIndex(),
        ];
    }

    public function persistEntity(EntityManagerInterface $entityManager, object $entityInstance): void
    {
        if ($entityInstance instanceof Utilisateur) {
            $this->hasherMotDePasse($entityInstance);
        }
        parent::persistEntity($entityManager, $entityInstance);
    }

    public function updateEntity(EntityManagerInterface $entityManager, object $entityInstance): void
    {
        if ($entityInstance instanceof Utilisateur) {
            $this->hasherMotDePasse($entityInstance);
        }
        parent::updateEntity($entityManager, $entityInstance);
    }

    private function hasherMotDePasse(Utilisateur $utilisateur): void
    {
        $motDePasse = $utilisateur->getPlainPassword();

        // Champ vide en édition : on garde le hash existant
        if ($motDePasse !== null && $motDePasse !== '') {
            $utilisateur->setPassword($this->passwordHasher->hashPassword($utilisateur, $motDePasse));
        }

        // On ne garde jamais le mot de passe en clair en mémoire
        $utilisateur->setPlainPassword(null);
    }
}
