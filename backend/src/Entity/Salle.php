<?php

namespace App\Entity;

use App\Repository\SalleRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: SalleRepository::class)]
class Salle
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 100)]
    private ?string $nom = null;

    #[ORM\Column(length: 100, nullable: true)]
    private ?string $ville = null;

    #[ORM\Column(length: 2, nullable: true)]
    private ?string $pays = null;

    #[ORM\Column]
    private ?bool $masquerCotationsRecentes = null;

    /**
     * @var Collection<int, Ouverture>
     */
    #[ORM\OneToMany(targetEntity: Ouverture::class, mappedBy: 'salle')]
    private Collection $ouvertures;

    public function __construct()
    {
        $this->ouvertures = new ArrayCollection();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getNom(): ?string
    {
        return $this->nom;
    }

    public function setNom(string $nom): static
    {
        $this->nom = $nom;

        return $this;
    }

    public function getVille(): ?string
    {
        return $this->ville;
    }

    public function setVille(?string $ville): static
    {
        $this->ville = $ville;

        return $this;
    }

    public function getPays(): ?string
    {
        return $this->pays;
    }

    public function setPays(?string $pays): static
    {
        $this->pays = $pays;

        return $this;
    }

    public function isMasquerCotationsRecentes(): ?bool
    {
        return $this->masquerCotationsRecentes;
    }

    public function setMasquerCotationsRecentes(bool $masquerCotationsRecentes): static
    {
        $this->masquerCotationsRecentes = $masquerCotationsRecentes;

        return $this;
    }

    /**
     * @return Collection<int, Ouverture>
     */
    public function getOuvertures(): Collection
    {
        return $this->ouvertures;
    }

    public function addOuverture(Ouverture $ouverture): static
    {
        if (!$this->ouvertures->contains($ouverture)) {
            $this->ouvertures->add($ouverture);
            $ouverture->setSalle($this);
        }

        return $this;
    }

    public function removeOuverture(Ouverture $ouverture): static
    {
        if ($this->ouvertures->removeElement($ouverture)) {
            // set the owning side to null (unless already changed)
            if ($ouverture->getSalle() === $this) {
                $ouverture->setSalle(null);
            }
        }

        return $this;
    }

    public function __toString(): string
    {
        return sprintf(
            '%s (%s)',
            $this->nom,
            $this->ville ?? 'Ville inconnue'
        );
    }
}
