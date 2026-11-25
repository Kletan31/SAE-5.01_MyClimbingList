<?php

namespace App\Controller\Api;

use App\Entity\Utilisateur;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Security\Http\Attribute\CurrentUser;

class MeController extends AbstractController
{
    #[Route('/api/me', name: 'api_me', methods: ['GET'])]
    public function me(#[CurrentUser] Utilisateur $utilisateur): JsonResponse
    {
        return $this->json([
            'id' => $utilisateur->getId(),
            'email' => $utilisateur->getEmail(),
            'nomUtilisateur' => $utilisateur->getNomUtilisateur(),
            'nom' => $utilisateur->getNom(),
            'prenom' => $utilisateur->getPrenom(),
            'genre' => $utilisateur->getGenre(),
            'langue' => $utilisateur->getLangue(),
            'dateInscription' => $utilisateur->getDateInscription()?->format(\DATE_ATOM),
            'salleFavoriteId' => $utilisateur->getSalleFavorite()?->getId(),
        ]);
    }
}
