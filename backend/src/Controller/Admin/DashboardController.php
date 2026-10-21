<?php

namespace App\Controller\Admin;

use App\Entity\Ouverture;
use App\Entity\Salle;
use App\Entity\Utilisateur;
use Doctrine\ORM\EntityManagerInterface;
use EasyCorp\Bundle\EasyAdminBundle\Attribute\AdminDashboard;
use EasyCorp\Bundle\EasyAdminBundle\Config\Dashboard;
use EasyCorp\Bundle\EasyAdminBundle\Config\MenuItem;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractDashboardController;
use Symfony\Component\HttpFoundation\Response;

#[AdminDashboard(routePath: '/admin', routeName: 'admin')]
class DashboardController extends AbstractDashboardController
{
    public function __construct(private EntityManagerInterface $em)
    {
    }

    public function index(): Response
    {
        return $this->render('admin/dashboard.html.twig', [
            'nbSalles' => $this->em->getRepository(Salle::class)->count([]),
            'nbOuvertures' => $this->em->getRepository(Ouverture::class)->count([]),
            'nbOuverturesActives' => $this->em->getRepository(Ouverture::class)->count(['statut' => 'actif']),
            'nbUtilisateurs' => $this->em->getRepository(Utilisateur::class)->count([]),
        ]);
    }

    public function configureDashboard(): Dashboard
    {
        return Dashboard::new()
            ->setTitle('My Climbing List - Administration');
    }

    public function configureMenuItems(): iterable
    {
        yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');
        yield MenuItem::linkTo(SalleCrudController::class, 'Salles', 'fas fa-building');
        yield MenuItem::linkTo(OuvertureCrudController::class, 'Ouvertures', 'fas fa-route');
        yield MenuItem::linkTo(UtilisateurCrudController::class, 'Utilisateurs', 'fas fa-users');
    }
}