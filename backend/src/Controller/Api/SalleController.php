<?php

namespace App\Controller\Api;

use App\Entity\Salle;
use App\Repository\SalleRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Attribute\Route;

class SalleController extends AbstractController
{
    #[Route('/api/salles', name: 'api_salles_liste', methods: ['GET'])]
    public function liste(SalleRepository $salles): JsonResponse
    {
        return $this->json(array_map(
            fn (Salle $s) => [
                'id' => $s->getId(),
                'nom' => $s->getNom(),
                'ville' => $s->getVille(),
                'pays' => $s->getPays(),
                'image' => $s->getImage(),
            ],
            $salles->findBy([], ['nom' => 'ASC'])
        ));
    }
}
