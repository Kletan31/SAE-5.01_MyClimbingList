<?php

namespace App\Entity;

use App\Enum\StatutOuverture;
use App\Enum\TypeOuverture;
use App\Repository\OuvertureRepository;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: OuvertureRepository::class)]
#[ORM\HasLifecycleCallbacks]
class Ouverture
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\ManyToOne(inversedBy: 'ouvertures')]
    #[ORM\JoinColumn(nullable: false)]
    private ?Salle $salle = null;

    #[ORM\Column(length: 5, enumType: TypeOuverture::class)]
    private ?TypeOuverture $type = null;

    #[ORM\Column(length: 50)]
    private ?string $cotation = null;

    #[ORM\Column(length: 50, nullable: true)]
    private ?string $couleur = null;

    #[ORM\Column(length: 11, nullable: true)]
    private ?string $couleurHex = null;

    #[ORM\Column(type: Types::DATE_IMMUTABLE)]
    private ?\DateTimeImmutable $dateCreation = null;

    #[ORM\Column(nullable: true)]
    private ?int $relais = null;

    #[ORM\Column(length: 100, nullable: true)]
    private ?string $secteur = null;

    #[ORM\Column(length: 10, enumType: StatutOuverture::class)]
    private StatutOuverture $statut = StatutOuverture::Actif;

    #[ORM\Column(type: Types::DATE_IMMUTABLE, nullable: true)]
    private ?\DateTimeImmutable $dateDemontage = null;

    #[ORM\Column(options: ['default' => false])]
    private bool $enTete = false;

    //! Provisoire : à remplacer plus tard
    #[ORM\Column(type: Types::JSON, nullable: true)]
    private ?array $proprietes = null;

    public function __construct()
    {
        $this->dateCreation = new \DateTimeImmutable();
    }

    // Un bloc ne peut jamais être fait en tête
    #[ORM\PrePersist]
    #[ORM\PreUpdate]
    public function normaliserEnTete(): void
    {
        if ($this->type === TypeOuverture::Bloc) {
            $this->enTete = false;
        }
    }

    public function getId(): ?int
    {
        return $this->id;
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

    public function getType(): ?TypeOuverture
    {
        return $this->type;
    }

    public function setType(TypeOuverture $type): static
    {
        $this->type = $type;

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

    public function getDateCreation(): ?\DateTimeImmutable
    {
        return $this->dateCreation;
    }

    public function setDateCreation(\DateTimeImmutable $dateCreation): static
    {
        $this->dateCreation = $dateCreation;

        return $this;
    }

    public function getRelais(): ?int
    {
        return $this->relais;
    }

    public function setRelais(?int $relais): static
    {
        $this->relais = $relais;

        return $this;
    }

    public function getSecteur(): ?string
    {
        return $this->secteur;
    }

    public function setSecteur(?string $secteur): static
    {
        $this->secteur = $secteur;

        return $this;
    }

    public function getStatut(): StatutOuverture
    {
        return $this->statut;
    }

    public function setStatut(StatutOuverture $statut): static
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

    public function isEnTete(): bool
    {
        return $this->enTete;
    }

    public function setEnTete(bool $enTete): static
    {
        $this->enTete = $enTete;

        return $this;
    }

    public function getProprietes(): ?array
    {
        return $this->proprietes;
    }

    public function setProprietes(?array $proprietes): static
    {
        $this->proprietes = $proprietes;

        return $this;
    }

    public function __toString(): string
    {
        return sprintf(
            '%s %s%s',
            $this->type?->value ?? '?',
            $this->cotation ?? '?',
            $this->couleur ? ' (' . $this->couleur . ')' : ''
        );
    }
}
