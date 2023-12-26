import pygame
import sys
import subprocess
from Variaveis import largura_tela,altura_tela


# Inicializar o Pygame
pygame.init()


tela = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN)
pygame.display.set_caption("Menu do Jogo")

# Carregar imagem de fundo do menu e redimensionar para preencher a tela
fundo_menu = pygame.image.load("Sprites/Menu_Of2.jpg")
fundo_menu = pygame.transform.scale(fundo_menu, (largura_tela, altura_tela))

# Cores
cor_botao_normal = (98, 222, 221)
cor_botao_selecionado = (255, 51, 106)
cor_letra = (255,169, 10)  # amarelo_tilulo
branco=(255,255,255) # Letras botões
cor_borda = (0, 0, 0)  # Azul

# Fonte do texto do botão
fonte = pygame.font.Font(None, 36)

# Fonte e configurações do título
caminho_fonte_titulo = "Top_Menu.otf"
tamanho_fonte_titulo = 72
fonte_titulo = pygame.font.Font(caminho_fonte_titulo, tamanho_fonte_titulo)

# Título do jogo
titulo_jogo = "Ruptura Temporal"

# Coordenadas para o título no topo da tela
posicao_titulo = (largura_tela // 2, altura_tela // 8)

# Lista de botões e índice do botão selecionado
opcoes = ["Iniciar Jornada", "Configurações", "Como Jogar", "Sair"]
indice_selecionado = 0

# Variáveis para a animação do botão selecionado
pulso_animacao = 2
pulso_crescente = True

# Loop principal do menu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                indice_selecionado = (indice_selecionado - 1) % len(opcoes)
            elif event.key == pygame.K_s:
                indice_selecionado = (indice_selecionado + 1) % len(opcoes)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if indice_selecionado == 0:
                    import GAME
                elif indice_selecionado == len(opcoes) - 1:
                    running = False  # Sair do programa se "Sair" for selecionado

    # Atualizar a animação do botão selecionado
    if pulso_crescente:
        pulso_animacao += 1
        if pulso_animacao >= 10:
            pulso_crescente = False
    else:
        pulso_animacao -= 700
        if pulso_animacao <= 400:
            pulso_crescente = True

    # Desenhar o menu
    tela.blit(fundo_menu, (0, 0))

    # Desenhar o título
    texto_titulo = fonte_titulo.render(titulo_jogo, True, cor_letra)
    retangulo_titulo = texto_titulo.get_rect(center=posicao_titulo)
    tela.blit(texto_titulo, retangulo_titulo)

    # Desenhar os botões
    for i, opcao in enumerate(opcoes):
        cor_botao = cor_botao_selecionado if i == indice_selecionado else cor_botao_normal
        retangulo_botao = pygame.Rect(largura_tela // 10 - 150, altura_tela // 2 + i * 60, 300, 40)

        # Adicionar efeito de pulsação ao botão selecionado
        pygame.draw.rect(tela, cor_botao, (retangulo_botao.left - pulso_animacao, retangulo_botao.top - pulso_animacao, retangulo_botao.width + 2 * pulso_animacao, retangulo_botao.height + 2 * pulso_animacao))
        pygame.draw.rect(tela, cor_botao, retangulo_botao)

        texto_botao = fonte.render(opcao, True, branco)
        # Obter o retângulo do texto e definir suas coordenadas para o centro do botão
        retangulo_texto = texto_botao.get_rect(center=retangulo_botao.center)
        # Desenhar o texto centrado no botão
        tela.blit(texto_botao, retangulo_texto)

    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()
sys.exit()
