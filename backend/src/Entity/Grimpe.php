<?php

namespace App\Entity;

use App\Entity\Trait\Horodatage;
use App\Repository\GrimpeRepository;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: GrimpeRepository::class)]
#[ORM\HasLifecycleCallbacks]
#[ORM\UniqueConstraint(name: 'UNIQ_GRIMPE_SEANCE_OUVERTURE', fields: ['seance', 'ouverture'])]
class Grimpe
{
    use Horodatage;

    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\ManyToOne(inversedBy: 'grimpes')]
    #[ORM\JoinColumn(nullable: false)]
    private ?Seance $seance = null;

    #[ORM\ManyToOne]
    #[ORM\JoinColumn(nullable: false)]
    private ?Ouverture $ouverture = null;

    #[ORM\Column(options: ['default' => 0])]
    private int $montee = 0;

    #[ORM\Column(options: ['default' => 0])]
    private int $top = 0;

    #[ORM\Column(options: ['default' => false])]
    private bool $flash = false;

    #[ORM\Column(options: ['default' => 0])]
    private int $monteeTete = 0;

    #[ORM\Column(options: ['default' => 0])]
    private int $topTete = 0;

    #[ORM\Column(options: ['default' => false])]
    private bool $flashTete = false;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getSeance(): ?Seance
    {
        return $this->seance;
    }

    public function setSeance(?Seance $seance): static
    {
        $this->seance = $seance;

        return $this;
    }

    public function getOuverture(): ?Ouverture
    {
        return $this->ouverture;
    }

    public function setOuverture(?Ouverture $ouverture): static
    {
        $this->ouverture = $ouverture;

        return $this;
    }

    public function getMontee(): int
    {
        return $this->montee;
    }

    public function setMontee(int $montee): static
    {
        $this->montee = $montee;

        return $this;
    }

    public function getTop(): int
    {
        return $this->top;
    }

    public function setTop(int $top): static
    {
        $this->top = $top;

        return $this;
    }

    public function isFlash(): bool
    {
        return $this->flash;
    }

    public function setFlash(bool $flash): static
    {
        $this->flash = $flash;

        return $this;
    }

    public function getMonteeTete(): int
    {
        return $this->monteeTete;
    }

    public function setMonteeTete(int $monteeTete): static
    {
        $this->monteeTete = $monteeTete;

        return $this;
    }

    public function getTopTete(): int
    {
        return $this->topTete;
    }

    public function setTopTete(int $topTete): static
    {
        $this->topTete = $topTete;

        return $this;
    }

    public function isFlashTete(): bool
    {
        return $this->flashTete;
    }

    public function setFlashTete(bool $flashTete): static
    {
        $this->flashTete = $flashTete;

        return $this;
    }

    public function __toString(): string
    {
        return sprintf('%s - %s', $this->seance ?? '?', $this->ouverture ?? '?');
    }
}
