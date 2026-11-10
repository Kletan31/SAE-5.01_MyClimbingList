<?php

namespace App\Entity;

use App\Entity\Trait\Horodatage;
use App\Repository\SeanceRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: SeanceRepository::class)]
#[ORM\HasLifecycleCallbacks]
#[ORM\UniqueConstraint(name: 'UNIQ_SEANCE_UTILISATEUR_SALLE_DATE', fields: ['utilisateur', 'salle', 'dateSeance'])]
class Seance
{
    use Horodatage;

    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\ManyToOne]
    #[ORM\JoinColumn(nullable: false)]
    private ?Utilisateur $utilisateur = null;

    #[ORM\ManyToOne]
    #[ORM\JoinColumn(nullable: false)]
    private ?Salle $salle = null;

    #[ORM\Column(type: Types::DATE_IMMUTABLE)]
    private ?\DateTimeImmutable $dateSeance = null;

    /**
     * @var Collection<int, Grimpe>
     */
    #[ORM\OneToMany(targetEntity: Grimpe::class, mappedBy: 'seance', orphanRemoval: true, cascade: ['persist'])]
    private Collection $grimpes;

    public function __construct()
    {
        $this->grimpes = new ArrayCollection();
        $this->dateSeance = new \DateTimeImmutable('today');
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getUtilisateur(): ?Utilisateur
    {
        return $this->utilisateur;
    }

    public function setUtilisateur(?Utilisateur $utilisateur): static
    {
        $this->utilisateur = $utilisateur;

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

    public function getDateSeance(): ?\DateTimeImmutable
    {
        return $this->dateSeance;
    }

    public function setDateSeance(\DateTimeImmutable $dateSeance): static
    {
        $this->dateSeance = $dateSeance;

        return $this;
    }

    /**
     * @return Collection<int, Grimpe>
     */
    public function getGrimpes(): Collection
    {
        return $this->grimpes;
    }

    public function addGrimpe(Grimpe $grimpe): static
    {
        if (!$this->grimpes->contains($grimpe)) {
            $this->grimpes->add($grimpe);
            $grimpe->setSeance($this);
        }

        return $this;
    }

    public function removeGrimpe(Grimpe $grimpe): static
    {
        if (($this->grimpes->removeElement($grimpe)) && ($grimpe->getSeance() === $this)) {
            $grimpe->setSeance(null);
        }

        return $this;
    }

    public function __toString(): string
    {
        return sprintf(
            '%s - %s - %s',
            $this->dateSeance?->format('d/m/Y') ?? '?',
            $this->salle?->getNom() ?? '?',
            $this->utilisateur ?? '?'
        );
    }
}
