import pygame
from ElementoJogo import ElementoJogo

class Nave(ElementoJogo):
    def __init__(self, largura_tela, altura_tela, velocidade=10, cor=(0, 255, 100)):
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
        self.vel_x = 0
        self.tiros = []  # Lista que guardará os tiros ativos

    def processar_evento(self, evento):
        """Controla os eventos de teclado para movimentação e disparo."""
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                self.vel_x = -self.velocidade
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self.vel_x = self.velocidade
            elif evento.key == pygame.K_SPACE:
                self.atirar()

        elif evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_a) and self.vel_x < 0:
                self.vel_x = 0
            elif evento.key in (pygame.K_RIGHT, pygame.K_d) and self.vel_x > 0:
                self.vel_x = 0
                
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LSHIFT:
                    self.velocidade += 20  # Aumenta a velocidade ao pressionar Shift)
            
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LSHIFT:
                self.velocidade -= 20  # Restaura a velocidade ao soltar Shift

    def mover(self):
        """Aplica o deslocamento horizontal e trava nas bordas da tela."""
        self.rect.x += self.vel_x

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.largura_tela:
            self.rect.right = self.largura_tela

    def atirar(self):
        # =========================================================================
        # TODO 1 (Alunos): Criar um projétil (pygame.Rect) saindo da ponta da nave
        # (ex: largura 4, altura 10) e adicioná-lo à lista self.tiros
        # =========================================================================
        tiro = pygame.Rect(self.rect.centerx - 2, self.rect.top, 4, 10)
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

        # Desenha os tiros
        for tiro in self.tiros:
            pygame.draw.rect(tela, (255, 0, 0), tiro)