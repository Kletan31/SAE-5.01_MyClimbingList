<?php

namespace App\Entity;

use App\Repository\OuvertureRepository;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: OuvertureRepository::class)]
class Ouverture
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 5)]
    private ?string $discipline = null;

    #[ORM\Column]
    private ?int $relais = null;

    #[ORM\Column(length: 50)]
    private ?string $cotation = null;

    #[ORM\Column(length: 50, nullable: true)]
    private ?string $couleur = null;

    #[ORM\Column(length: 11, nullable: true)]
    private ?string $couleurHex = null;

    #[ORM\Column(type: Types::DATE_IMMUTABLE)]
    private ?\DateTimeImmutable $dateOuverture = null;

    #[ORM\Column(length: 10)]
    private ?string $statut = 'actif';

    #[ORM\Column(type: Types::DATE_IMMUTABLE, nullable: true)]
    private ?\DateTimeImmutable $dateDemontage = null;

    #[ORM\ManyToOne(inversedBy: 'ouvertures')]
    #[ORM\JoinColumn(nullable: false)]
    private ?Salle $salle = null;

    public function __construct()
    {
        $this->dateOuverture = new \DateTimeImmutable();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getDiscipline(): ?string
    {
        return $this->discipline;
    }

    public function setDiscipline(string $discipline): static
    {
        $this->discipline = $discipline;

        return $this;
    }

    public function getRelais(): ?int
    {
        return $this->relais;
    }

    public function setRelais(int $relais): static
    {
        $this->relais = $relais;

        return $this;
    }

    public function getCotation(): ?string
    {
        return $this->cotation;
    }

    public function setCotation(string $cotation): static
    {
        $this->cotation = $cotation;

        return $this;
    }

    public function getCouleur(): ?string
    {
        return $this->couleur;
    }

    public function setCouleur(?string $couleur): static
    {
        $this->couleur = $couleur;

        return $this;
    }

    public function getCouleurHex(): ?string
    {
        return $this->couleurHex;
    }

    public function setCouleurHex(?string $couleurHex): static
    {
        $this->couleurHex = $couleurHex;

        return $this;
    }

    public function getDateOuverture(): ?\DateTimeImmutable
    {
        return $this->dateOuverture;
    }

    public function setDateOuverture(\DateTimeImmutable $dateOuverture): static
    {
        $this->dateOuverture = $dateOuverture;

        return $this;
    }

    public function getStatut(): ?string
    {
        return $this->statut;
    }

    public function setStatut(string $statut): static
    {
        $this->statut = $statut;

        return $this;
    }

    public function getDateDemontage(): ?\DateTimeImmutable
    {
        return $this->dateDemontage;
    }

    public function setDateDemontage(?\DateTimeImmutable $dateDemontage): static
    {
        $this->dateDemontage = $dateDemontage;

        return $this;
    }

    public function getSalle(): ?Salle
    {
        return $this->salle;
    }

    public function setSalle(?Salle $salle): static
    {
        $this->salle = $salle;

        return $this;
    }
}
