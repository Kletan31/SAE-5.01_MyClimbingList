<?php

namespace App\Tests\Api;

use App\Tests\ApiTestCase;

class AuthEtProfilTest extends ApiTestCase
{
    public function testLoginRenvoieUnJeton(): void
    {
        $this->creerUtilisateur('a@test.fr', 'secret-12345');

        $this->requeteJson('POST', '/api/auth/login', ['email' => 'a@test.fr', 'password' => 'secret-12345']);

        $this->assertResponseStatusCodeSame(200);
        $this->assertNotEmpty($this->reponseJson()['token']);
    }

    public function testLoginAvecMauvaisMotDePasseRenvoie401(): void
    {
        $this->creerUtilisateur('a@test.fr', 'secret-12345');

        $this->requeteJson('POST', '/api/auth/login', ['email' => 'a@test.fr', 'password' => 'faux']);

        $this->assertResponseStatusCodeSame(401);
    }

    public function testMeSansJetonRenvoie401(): void
    {
        $this->requeteJson('GET', '/api/me');

        $this->assertResponseStatusCodeSame(401);
    }

    public function testMeAvecJetonFalsifieRenvoie401(): void
    {
        $this->requeteJson('GET', '/api/me', jeton: 'eyJhbGciOiJSUzI1NiJ9.bidon.signature');

        $this->assertResponseStatusCodeSame(401);
    }

    public function testMeRenvoieLeProfilSansDonneesSensibles(): void
    {
        $this->creerUtilisateur('a@test.fr', 'secret-12345');
        $jeton = $this->obtenirJeton('a@test.fr', 'secret-12345');

        $this->requeteJson('GET', '/api/me', jeton: $jeton);

        $this->assertResponseStatusCodeSame(200);
        $profil = $this->reponseJson();
        $this->assertSame('a@test.fr', $profil['email']);
        $this->assertArrayNotHasKey('password', $profil);
        $this->assertArrayNotHasKey('roles', $profil);
    }

    public function testSallesAccessiblesSansJeton(): void
    {
        $this->requeteJson('GET', '/api/salles');

        $this->assertResponseStatusCodeSame(200);
        $this->assertIsArray($this->reponseJson());
    }
}
