import pygame
import sys

# Definição das constantes
LARGURA = 600
ALTURA = 600
LINHAS = 3
COLUNAS = 3
TAMANHO_CELULA = LARGURA // COLUNAS
BORDA = 50
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Inicialização do Pygame
pygame.init()

# Classe para representar cada célula do tabuleiro
class Celula:
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.simbolo = ' '
        self.proxima = None

# Classe para representar o tabuleiro do jogo
class Tabuleiro:
    def __init__(self):
        self.celulas = [[Celula(linha, coluna) for coluna in range(COLUNAS)] for linha in range(LINHAS)]
        self.vencedor = None

    # Função para desenhar o tabuleiro
    def desenhar(self, tela):
        tela.fill(BRANCO)
        for linha in range(1, LINHAS):
            pygame.draw.line(tela, PRETO, (0, linha * TAMANHO_CELULA), (LARGURA, linha * TAMANHO_CELULA), 2)
        for coluna in range(1, COLUNAS):
            pygame.draw.line(tela, PRETO, (coluna * TAMANHO_CELULA, 0), (coluna * TAMANHO_CELULA, ALTURA), 2)

    # Função para desenhar os símbolos
    def desenhar_simbolos(self, tela):
        for linha in self.celulas:
            for celula in linha:
                if celula.simbolo == 'X':
                    pygame.draw.line(tela, VERMELHO, (celula.coluna * TAMANHO_CELULA + BORDA, celula.linha * TAMANHO_CELULA + BORDA),
                                    ((celula.coluna + 1) * TAMANHO_CELULA - BORDA, (celula.linha + 1) * TAMANHO_CELULA - BORDA), 5)
                    pygame.draw.line(tela, VERMELHO, ((celula.coluna + 1) * TAMANHO_CELULA - BORDA, celula.linha * TAMANHO_CELULA + BORDA),
                                    (celula.coluna * TAMANHO_CELULA + BORDA, (celula.linha + 1) * TAMANHO_CELULA - BORDA), 5)
                elif celula.simbolo == 'O':
                    pygame.draw.circle(tela, AZUL, (celula.coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2,
                                                    celula.linha * TAMANHO_CELULA + TAMANHO_CELULA // 2), TAMANHO_CELULA // 2 - BORDA, 5)

    # Função para verificar se há um vencedor
    def verificar_vencedor(self):
        # Verifica linhas e colunas
        for linha in range(LINHAS):
            if self.celulas[linha][0].simbolo == self.celulas[linha][1].simbolo == self.celulas[linha][2].simbolo != ' ':
                self.vencedor = self.celulas[linha][0].simbolo
                return True
            if self.celulas[0][linha].simbolo == self.celulas[1][linha].simbolo == self.celulas[2][linha].simbolo != ' ':
                self.vencedor = self.celulas[0][linha].simbolo
                return True

        # Verifica diagonais
        if self.celulas[0][0].simbolo == self.celulas[1][1].simbolo == self.celulas[2][2].simbolo != ' ':
            self.vencedor = self.celulas[0][0].simbolo
            return True
        if self.celulas[0][2].simbolo == self.celulas[1][1].simbolo == self.celulas[2][0].simbolo != ' ':
            self.vencedor = self.celulas[0][2].simbolo
            return True

        return False

    # Função para verificar se há um empate
    def verificar_empate(self):
        for linha in self.celulas:
            for celula in linha:
                if celula.simbolo == ' ':
                    return False
        return True

# Função principal
def main():
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption('Jogo da Velha')

    tabuleiro = Tabuleiro()
    jogador_atual = 'X'
    jogo_ativo = True

    while jogo_ativo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and tabuleiro.vencedor is None:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                coluna_clicada = mouseX // TAMANHO_CELULA
                linha_clicada = mouseY // TAMANHO_CELULA

                if tabuleiro.celulas[linha_clicada][coluna_clicada].simbolo == ' ':
                    tabuleiro.celulas[linha_clicada][coluna_clicada].simbolo = jogador_atual
                    if tabuleiro.verificar_vencedor():
                        print(f"O jogador {tabuleiro.vencedor} ganhou!")
                        jogo_ativo = False
                    elif tabuleiro.verificar_empate():
                        print("Empate!")
                        jogo_ativo = False
                    else:
                        jogador_atual = 'O' if jogador_atual == 'X' else 'X'

        tabuleiro.desenhar(tela)
        tabuleiro.desenhar_simbolos(tela)
        pygame.display.update()

    print("Fim do jogo.")
    if jogar_novamente():
        main()
    else:
        pygame.quit()
        sys.exit()

# Função para jogar novamente ou sair
def jogar_novamente():
    while True:
        resposta = input("Deseja jogar novamente? (S/N): ").strip().lower()
        if resposta == 's':
            return True
        elif resposta == 'n':
            return False
        else:
            print("Resposta inválida. Por favor, responda 'S' para Sim ou 'N' para Não.")

# Início do jogo
main()