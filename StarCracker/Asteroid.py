import random
import pygame
from ElementoJogo import ElementoJogo


class Asteroid(ElementoJogo):
    def __init__(self, largura_tela, altura_tela, velocidade=8, cor=(81, 81, 85)):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.raio = 20
        self.dano = 0
        self.dificuldade = 0  # Aumenta conforme a pontuação (deixa os asteroides mais rápidos)

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
    

        # Posição aleatória
        self.rect.x = random.randint(
            0,
            self.largura_tela - self.rect.width
        )

        # Acima da tela
        self.rect.y = random.randint(-150, -50)

        # Velocidade aleatória. A mínima é 3 para garantir que TODO asteroide se mova.
        # Fica maior conforme a dificuldade (pontuação) sobe: a cada 5 pontos ganha +1,
        # com limite de +8 para não ficar impossível.
        extra = self.dificuldade // 5
        if extra > 8:
            extra = 8
        self.velocidade = random.randint(3, 7) + extra

        # Reinicia o dano
        self.dano = 0

        # Cor inicial
        self.cor = (100, 100, 100)

    def mover(self):
        self.rect.y += self.velocidade

        # Reinicia no topo caso passe reto pelo fundo da tela
        if self.rect.top > self.altura_tela:
            self.iniciar_status()

    def desenhar(self, tela):
        

        x = self.rect.centerx
        y = self.rect.centery

        # Formato irregular de pedra
        pontos = [
            (x - 15, y - 20),
            (x + 10, y - 18),
            (x + 22, y - 5),
            (x + 18, y + 15),
            (x, y + 22),
            (x - 20, y + 12),
            (x - 25, y - 5)
        ]

        # Pedra
        pygame.draw.polygon(
            tela,
            self.cor,
            pontos
        )

        # Crateras / detalhes
        pygame.draw.circle(
            tela,
            (60, 60, 60),
            (x - 8, y - 5),
            4
        )

        pygame.draw.circle(
            tela,
            (60, 60, 60),
            (x + 8, y + 8),
            3
        )