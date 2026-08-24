import pygame
from ElementoJogo import ElementoJogo

class Nave(ElementoJogo):
    def __init__(self, largura_tela, altura_tela, velocidade=6, cor=(0, 255, 100)):
        # Inicializa a classe base com posição inicial centralizada embaixo
        super().__init__(
            x=largura_tela // 2 - 30,
            y=altura_tela - 70,
            largura=60,
            altura=50,
            cor=cor,
            velocidade=velocidade
        )
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.direcao = 0  # -1 = esquerda, 0 = parado, 1 = direita
        self.turbo = False  # Shift ligado (True) ou desligado (False)
        self.tiros = []  # Lista que guardará os tiros ativos

    def processar_evento(self, evento):
        """Controla os eventos de teclado para movimentação e disparo."""
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                self.direcao = -1
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self.direcao = 1
            elif evento.key == pygame.K_SPACE:
                self.atirar()
            elif evento.key == pygame.K_LSHIFT:
                self.turbo = True  # Liga o turbo enquanto o Shift estiver pressionado

        elif evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_a) and self.direcao == -1:
                self.direcao = 0
            elif evento.key in (pygame.K_RIGHT, pygame.K_d) and self.direcao == 1:
                self.direcao = 0
            elif evento.key == pygame.K_LSHIFT:
                self.turbo = False  # Desliga o turbo ao soltar o Shift

    def mover(self):
        """Aplica o deslocamento horizontal e trava nas bordas da tela."""
        # A velocidade é calculada AQUI, a cada quadro. Por isso o turbo
        # funciona na hora, mesmo se a nave já estiver se movendo.
        velocidade_atual = self.velocidade
        if self.turbo:
            velocidade_atual = self.velocidade * 2  # Dobra a velocidade com o Shift

        self.rect.x += self.direcao * velocidade_atual

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.largura_tela:
            self.rect.right = self.largura_tela

    def atirar(self):
        # =========================================================================
        # TODO 1 (Alunos): Criar um projétil (pygame.Rect) saindo da ponta da nave
        # (ex: largura 4, altura 10) e adicioná-lo à lista self.tiros
        # =========================================================================
        tiro = pygame.Rect(self.rect.centerx - 3, self.rect.top, 6, 18)
        self.tiros.append(tiro)
        pass

    def atualizar_tiros(self):
        # =========================================================================
        # TODO 2 (Alunos):
        # - Mover cada tiro da lista para cima (diminuir tiro.y)
        # - Remover da lista os tiros que saírem pelo topo da tela (tiro.bottom < 0)
        # =========================================================================
        for tiro in self.tiros[:]:  # Verifica cada tiro na lista
            tiro.y -= 20  # Move o tiro para cima (velocidade de 20 pixels por frame)
            if tiro.bottom < 0:  # Se o tiro saiu da tela
                self.tiros.remove(tiro)  # Remove o tiro da lista
        pass

    def atualizar(self):
        self.mover()
        self.atualizar_tiros()

    def desenhar(self, tela):

        # Corpo principal da nave
        pygame.draw.circle(
            tela,
            self.cor,
            self.rect.center,
            25
        )

        # Parte frontal da nave
        frente_esquerda = [
            (self.rect.centerx - 25, self.rect.centery - 8),
            (self.rect.left - 10, self.rect.top),
            (self.rect.left - 10, self.rect.centery)
        ]

        frente_direita = [
            (self.rect.centerx + 25, self.rect.centery - 8),
            (self.rect.right + 10, self.rect.top),
            (self.rect.right + 10, self.rect.centery)
        ]

        pygame.draw.polygon(tela, self.cor, frente_esquerda)
        pygame.draw.polygon(tela, self.cor, frente_direita)

        # Cabine
        pygame.draw.rect(
            tela,
            (100, 150, 255),
            (
                self.rect.right - 8,
                self.rect.centery - 10,
                12,
                10
            )
        )

        # Detalhes do corpo
        pygame.draw.circle(
            tela,
            (80, 80, 80),
            self.rect.center,
            12,
            2
        )

        # Desenha os tiros como raios de laser com rastro de partículas
        for tiro in self.tiros:
            cx = tiro.centerx  # centro horizontal do tiro

            # 1) Rastro de partículas (fica ATRÁS do tiro, ou seja, um pouco abaixo).
            #    Vai do mais fraco/distante ao mais forte/perto do tiro.
            pygame.draw.circle(tela, (120, 30, 0), (cx, tiro.bottom + 14), 2)
            pygame.draw.circle(tela, (200, 70, 0), (cx, tiro.bottom + 8), 3)
            pygame.draw.circle(tela, (255, 140, 0), (cx, tiro.bottom + 3), 4)

            # 2) Brilho (glow) na ponta da frente do tiro
            pygame.draw.circle(tela, (255, 90, 0), (cx, tiro.top), 7)

            # 3) Corpo do raio (laranja/vermelho)
            pygame.draw.rect(tela, (255, 70, 0), tiro)

            # 4) Núcleo brilhante no centro (branco/amarelo), deixa com cara de energia
            nucleo = pygame.Rect(cx - 1, tiro.top, 2, tiro.height)
            pygame.draw.rect(tela, (255, 255, 200), nucleo)