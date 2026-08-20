import random
import pygame
from ElementoJogo import ElementoJogo


class Asteroid(ElementoJogo):
    def __init__(self, largura_tela, altura_tela, velocidade=8, cor=(81, 81, 85)):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.raio = 20

        super().__init__(
            x=0,
            y=0,
            largura=self.raio * 2,
            altura=self.raio * 2,
            cor=cor,
            velocidade=velocidade
        )
        self.iniciar_status()

    def iniciar_status(self):
        # =========================================================================
        # TODO 3 (Alunos):
        # - Sortear uma posição X aleatória dentro dos limites da tela
        # - Posicionar o Y acima da tela (ex: entre -150 e -50)
        # - Sortear uma velocidade de queda aleatória (ex: entre 3 e 7)
        # =========================================================================
        self.rect.x = random.randint(0, self.largura_tela - self.rect.width)
        self.rect.y = random.randint(-150, -50)
        self.velocidade = random.randint(10, 50)
        pass

    def mover(self):
        self.rect.y += self.velocidade

        # Reinicia no topo caso passe reto pelo fundo da tela
        if self.rect.top > self.altura_tela:
            self.iniciar_status()

    def desenhar(self, tela):
        # Polimorfismo: desenha o asteroide como círculo
        pygame.draw.circle(tela, self.cor, self.rect.center, self.raio)