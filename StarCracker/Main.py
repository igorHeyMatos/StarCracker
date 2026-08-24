import random

import pygame
from Nave import Nave
from Asteroid import Asteroid


class Jogo:
    def __init__(self):
        pygame.init()

        # ---- TELA CHEIA ----
        # Descobre o tamanho do monitor e cria a tela do tamanho dele.
        info = pygame.display.Info()
        self.largura = info.current_w
        self.altura = info.current_h
        self.tela = pygame.display.set_mode(
            (self.largura, self.altura), pygame.FULLSCREEN
        )
        pygame.display.set_caption("StarCracker")

        self.clock = pygame.time.Clock()
        self.fps = 30
        self.rodando = True
        self.game_over = False
        self.pontos = 0

        # ---- FONTES (para escrever texto na tela) ----
        self.fonte = pygame.font.SysFont("Arial", 36)
        self.fonte_grande = pygame.font.SysFont("Arial", 72)

        # ---- FUNDO DE ESTRELAS (temática Star Wars) ----
        # Cada estrela é uma lista [x, y]. Sorteamos 120 estrelas na tela.
        self.estrelas = []
        for i in range(120):
            x = random.randint(0, self.largura)
            y = random.randint(0, self.altura)
            self.estrelas.append([x, y])

        # ---- ELEMENTOS DO JOGO ----
        self.nave = Nave(self.largura, self.altura)

        # Vários asteroides ao mesmo tempo (guardados em uma lista).
        self.qtd_asteroides = 4
        self.asteroides = []
        for i in range(self.qtd_asteroides):
            self.asteroides.append(Asteroid(self.largura, self.altura))

        # Explosões ativas. Cada explosão é uma lista [x, y, raio].
        self.explosoes = []

    def reiniciar(self):
        """Zera a partida para o jogador jogar de novo (botão Retry)."""
        self.pontos = 0
        self.game_over = False
        self.explosoes = []
        self.nave = Nave(self.largura, self.altura)
        self.asteroides = []
        for i in range(self.qtd_asteroides):
            self.asteroides.append(Asteroid(self.largura, self.altura))

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            # ESC fecha o jogo (na tela cheia não há botão de fechar)
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.rodando = False
            self.nave.processar_evento(evento)

    def checar_colisoes(self):
        # =========================================================================
        # TODO 4 (Alunos):
        # A) Tiro vs Asteroide:
        #    - Percorrer self.nave.tiros
        #    - Se tiro.colliderect(self.asteroide.rect):
        #        1. Remover o tiro da lista
        #        2. Reiniciar o asteroide (self.asteroide.iniciar_status())
        #        3. Incrementar self.pontos em 1
        #
        # B) Asteroide vs Nave:
        #    - Se self.nave.rect.colliderect(self.asteroide.rect):
        #        - Finalizar a partida (self.rodando = False ou reiniciar)
        # =========================================================================
        self.nave.atualizar_tiros()  # Atualiza a posição dos tiros antes de verificar colisões

        # Verifica cada asteroide contra os tiros e contra a nave
        for asteroide in self.asteroides:
            # Se já está explodindo, ignora colisões (não conta ponto de novo)
            if asteroide.explodindo:
                continue

            for tiro in self.nave.tiros[:]:  # Itera sobre uma cópia dos tiros
                if tiro.colliderect(asteroide.rect):
                    self.nave.tiros.remove(tiro)  # Remove o tiro da lista
                    asteroide.explodir()  # Começa a ficar vermelho e sumir
                    # Cria uma explosão na posição do asteroide (x, y, raio inicial)
                    self.explosoes.append(
                        [asteroide.rect.centerx, asteroide.rect.centery, 5]
                    )
                    self.pontos += 1  # Incrementa os pontos
                    break  # Um tiro basta para destruir; sai do loop de tiros

            # Só encerra a partida se o asteroide NÃO estiver explodindo
            if not asteroide.explodindo and self.nave.rect.colliderect(asteroide.rect):
                self.game_over = True  # Mostra a tela de Game Over (não fecha o jogo)

    def atualizar(self):
        self.nave.atualizar()
        for asteroide in self.asteroides:
            asteroide.dificuldade = self.pontos  # Passa a pontuação (deixa mais rápido com o tempo)
            asteroide.mover()
        self.checar_colisoes()

    def desenhar_fundo(self):
        """Desenha o fundo preto e as estrelas descendo (efeito de viagem espacial)."""
        self.tela.fill((10, 10, 20))
        for estrela in self.estrelas:
            pygame.draw.circle(self.tela, (255, 255, 255), (estrela[0], estrela[1]), 2)
            estrela[1] += 2  # move a estrela para baixo
            # Quando a estrela sai por baixo, ela volta para o topo em outra posição
            if estrela[1] > self.altura:
                estrela[1] = 0
                estrela[0] = random.randint(0, self.largura)

    def desenhar_pontuacao(self):
        """Escreve a pontuação no canto superior direito da tela."""
        texto = self.fonte.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        self.tela.blit(texto, (self.largura - texto.get_width() - 20, 20))

    def desenhar_explosoes(self):
        """Desenha e anima as explosões: círculos que crescem e depois somem."""
        for explosao in self.explosoes[:]:  # cópia da lista para remover com segurança
            x = explosao[0]
            y = explosao[1]
            raio = explosao[2]

            # Dois círculos: um miolo claro e um anel externo, dando cara de explosão
            pygame.draw.circle(self.tela, (255, 200, 0), (x, y), raio // 2)   # miolo amarelo
            pygame.draw.circle(self.tela, (255, 90, 0), (x, y), raio, 3)      # anel laranja

            explosao[2] += 4  # cresce a cada quadro (a animação)
            if explosao[2] > 40:  # quando fica grande demais, some
                self.explosoes.remove(explosao)

    def desenhar(self):
        self.desenhar_fundo()
        self.nave.desenhar(self.tela)
        for asteroide in self.asteroides:
            asteroide.desenhar(self.tela)
        self.desenhar_explosoes()
        self.desenhar_pontuacao()
        pygame.display.flip()

    def tela_game_over(self):
        """Mostra a tela de Game Over com as opções Retry (R) e Exit (ESC)."""
        # Desenha o fundo com estrelas e os textos
        self.desenhar_fundo()

        texto1 = self.fonte_grande.render("GAME OVER", True, (255, 0, 0))
        texto2 = self.fonte.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        texto3 = self.fonte.render("R = Jogar de novo     ESC = Sair", True, (255, 255, 255))

        self.tela.blit(texto1, (self.largura // 2 - texto1.get_width() // 2, self.altura // 2 - 100))
        self.tela.blit(texto2, (self.largura // 2 - texto2.get_width() // 2, self.altura // 2))
        self.tela.blit(texto3, (self.largura // 2 - texto3.get_width() // 2, self.altura // 2 + 60))
        pygame.display.flip()

        # Verifica se o jogador apertou R (reiniciar) ou ESC (sair)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    self.reiniciar()
                elif evento.key == pygame.K_ESCAPE:
                    self.rodando = False

    def executar(self):
        while self.rodando:
            self.clock.tick(self.fps)
            if self.game_over:
                self.tela_game_over()
            else:
                self.processar_eventos()
                self.atualizar()
                self.desenhar()

        pygame.quit()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
