import random
import pygame
from ElementoJogo import ElementoJogo


class Asteroid(ElementoJogo):
    def __init__(self, largura_tela, altura_tela, velocidade=8, cor=(81, 81, 85)):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.raio = 20
        self.dano = 0
        self.explodindo = False  # True enquanto toca a animação de morte (fica vermelho e some)
        self.tempo_explosao = 0  # Contador de quadros da animação de morte
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
        # com limite de +5 para não ficar rápido demais e dar tempo de alcançar.
        extra = self.dificuldade // 5
        if extra > 5:
            extra = 5
        self.velocidade = random.randint(3, 5) + extra

        # Reinicia o dano e o estado de explosão
        self.dano = 0
        self.explodindo = False
        self.tempo_explosao = 0

        # Cor inicial (cinza)
        self.cor = (100, 100, 100)

    def explodir(self):
        """Começa a animação de morte: o asteroide vai ficar vermelho e sumir."""
        self.explodindo = True
        self.tempo_explosao = 6  # dura 6 quadros

    def mover(self):
        # Se está explodindo, faz a animação de cor (gradiente até o vermelho) e NÃO cai.
        if self.explodindo:
            self.tempo_explosao -= 1
            # O verde diminui de 120 até 0 -> a cor vai de laranja para vermelho intenso
            verde = self.tempo_explosao * 20
            self.cor = (255, verde, 0)
            if self.tempo_explosao <= 0:
                self.iniciar_status()  # renasce no topo (e para de explodir)
            return

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