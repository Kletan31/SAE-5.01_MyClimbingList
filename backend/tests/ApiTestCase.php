<?php

namespace App\Tests;

use App\Entity\Utilisateur;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\KernelBrowser;
use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

abstract class ApiTestCase extends WebTestCase
{
    protected KernelBrowser $client;

    protected function setUp(): void
    {
        $this->client = static::createClient();
    }

    protected function creerUtilisateur(
        string $email = 'grimpeur@test.fr',
        string $motDePasse = 'mot-de-passe-test',
        array $roles = [],
    ): Utilisateur {
        $conteneur = static::getContainer();
        $em = $conteneur->get(EntityManagerInterface::class);
        $hasher = $conteneur->get(UserPasswordHasherInterface::class);

        $utilisateur = (new Utilisateur())
            ->setEmail($email)
            ->setNomUtilisateur(explode('@', $email)[0])
            ->setRoles($roles);
        $utilisateur->setPassword($hasher->hashPassword($utilisateur, $motDePasse));

        $em->persist($utilisateur);
        $em->flush();

        return $utilisateur;
    }

    protected function requeteJson(string $methode, string $uri, ?array $corps = null, ?string $jeton = null): void
    {
        $serveur = ['CONTENT_TYPE' => 'application/json', 'HTTP_ACCEPT' => 'application/json'];
        if ($jeton !== null) {
            $serveur['HTTP_AUTHORIZATION'] = 'Bearer ' . $jeton;
        }

        $this->client->request(
            $methode,
            $uri,
            server: $serveur,
            content: $corps !== null ? json_encode($corps) : null,
        );
    }

    protected function obtenirJeton(string $email, string $motDePasse): string
    {
        $this->requeteJson('POST', '/api/auth/login', ['email' => $email, 'password' => $motDePasse]);

        return $this->reponseJson()['token'];
    }

    protected function reponseJson(): array
    {
        return json_decode($this->client->getResponse()->getContent(), true, flags: JSON_THROW_ON_ERROR);
    }
}
