<?php
namespace App\Entity\Trait;

use Doctrine\ORM\Mapping as ORM;

trait Horodatage
{
    #[ORM\Column]
    private ?\DateTimeImmutable $creeLe = null;

    #[ORM\Column]
    private ?\DateTimeImmutable $modifieLe = null;

    #[ORM\PrePersist]
    public function initTimestamps(): void
    {
        $this->creeLe ??= new \DateTimeImmutable();
        $this->modifieLe = $this->creeLe;
    }

    #[ORM\PreUpdate]
    public function touchModifieLe(): void
    {
        $this->modifieLe = new \DateTimeImmutable();
    }

    public function getCreeLe(): ?\DateTimeImmutable { return $this->creeLe; }
    public function getModifieLe(): ?\DateTimeImmutable { return $this->modifieLe; }
}
