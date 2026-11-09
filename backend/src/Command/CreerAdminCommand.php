<?php

namespace App\Command;

use App\Entity\Utilisateur;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

#[AsCommand(name: 'app:creer-admin', description: 'Crée un compte Direction pour accéder au backoffice')]
class CreerAdminCommand extends Command
{
    public function __construct(
        private EntityManagerInterface $em,
        private UserPasswordHasherInterface $passwordHasher,
    ) {
        parent::__construct();
    }

    protected function configure(): void
    {
        $this
            ->addArgument('email', InputArgument::REQUIRED, 'Email (identifiant de connexion)')
            ->addArgument('nom-utilisateur', InputArgument::REQUIRED, "Nom d'utilisateur (pseudo)");
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);

        $email = $input->getArgument('email');
        $pseudo = $input->getArgument('nom-utilisateur');

        $repo = $this->em->getRepository(Utilisateur::class);
        if ($repo->findOneBy(['email' => $email]) || $repo->findOneBy(['nomUtilisateur' => $pseudo])) {
            $io->error('Un utilisateur avec cet email ou ce nom d\'utilisateur existe déjà.');

            return Command::FAILURE;
        }

        $motDePasse = $io->askHidden('Mot de passe');
        if ($motDePasse === null || $motDePasse === '') {
            $io->error('Le mot de passe ne peut pas être vide.');

            return Command::FAILURE;
        }

        $utilisateur = (new Utilisateur())
            ->setEmail($email)
            ->setNomUtilisateur($pseudo)
            ->setRoles(['ROLE_DIRECTION']);
        $utilisateur->setPassword($this->passwordHasher->hashPassword($utilisateur, $motDePasse));

        $this->em->persist($utilisateur);
        $this->em->flush();

        $io->success(sprintf('Compte Direction créé pour %s.', $email));

        return Command::SUCCESS;
    }
}
