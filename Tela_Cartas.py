import pygame
import sys
from Deck import frames_por ,frames_trembo ,frames_sec
from Variaveis import largura_mapa, altura_mapa,largura_tela, altura_tela
import time
velocidade_personagem=8
intervalo_disparo = 8 #velocidade do player

escolha_jogador = None
def tela_de_pausa():
    global velocidade_personagem,intervalo_disparo
    frame_atual = 0
    #########################################################################################################
    
    pausa = True

    # Posições para exibir as imagens das cartas
    last_frame_time = time.time() * 1000  # Multiplicamos por 1000 para converter segundos para milissegundos
    tela_pausa = pygame.display.set_mode((largura_mapa, altura_mapa))
    pygame.display.set_caption("Tela de Atributos")
    while pausa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                # Exibir imagens das cartas

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    escolha_jogador = 1
                    print("SINTA MINHA IRÁ")
                    intervalo_disparo = max(100, intervalo_disparo - 8.5)
                    pausa = False
            
                    
                elif event.key == pygame.K_2:
                    escolha_jogador = 2
                    print("ESTOU QUASE FLUTUANDO")
                    velocidade_personagem += 20


                    pausa = False
                    
                if event.key == pygame.K_KP_1:
                    escolha_jogador = 1
                    print("SINTA MINHA IRÁ")
                    intervalo_disparo = max(100, intervalo_disparo - 8.5)
                    pausa = False
                    
                elif event.key == pygame.K_KP_2:
                    escolha_jogador = 2
                    print("ESTOU QUASE FLUTUANDO")
                    pausa = False
                    velocidade_personagem += 20
                    
                
            # Exibir imagens das cartas
           
                
                    

            tela_pausa.fill((255, 255, 255))
            fonte = pygame.font.Font(None, 36)
            cor_do_texto = (0, 255, 255)  # Cor preta

            texto_titulo = fonte.render("Escolha um atributo:", True, cor_do_texto)
            texto_opcoes = fonte.render("1 - Ódio Profundo   2 - Botas do Poder", True, cor_do_texto)

            # Centraliza o texto no meio da tela
            pos_titulo = ((largura_mapa - texto_titulo.get_width()) // 2, altura_mapa // 2 - 100)
            pos_opcoes = ((largura_mapa - texto_opcoes.get_width()) // 2, altura_mapa // 2 - 50)

        
        
        ########################################################################## Lógica para alternar entre os frames da animação
        current_time = time.time() * 1000
        if current_time - last_frame_time > 500:  # Trocar de frame a cada 500 milissegundos (0.5 segundos)
            frame_atual = (frame_atual + 1) % len(frames_trembo)
            last_frame_time = current_time

        carta_odio = pygame.image.load(frames_trembo[frame_atual])
        carta_por = pygame.image.load(frames_por[frame_atual])
        carta_sec = pygame.image.load(frames_sec[frame_atual])

        escala_carta = 2.0  # Fator de escala

        # Redimensione as cartas antes de renderizá-las na tela
        carta_odio_redimensionada = pygame.transform.scale(carta_odio,
                                                           (int(carta_odio.get_width() * escala_carta),
                                                            int(carta_odio.get_height() * escala_carta)))
        carta_por_redimensionada = pygame.transform.scale(carta_por,
                                                           (int(carta_por.get_width() * escala_carta),
                                                            int(carta_por.get_height() * escala_carta)))
        carta_sec_redimensionada = pygame.transform.scale(carta_sec,
                                                           (int(carta_sec.get_width() * escala_carta),
                                                            int(carta_sec.get_height() * escala_carta)))

         # Renderize as cartas redimensionadas na tela
        tela_pausa.blit(carta_odio_redimensionada, ((largura_mapa - carta_odio_redimensionada.get_width()) // 2,
                                                    altura_mapa // 2 + 100))
        
        tela_pausa.blit(carta_por_redimensionada, ((largura_mapa - carta_por_redimensionada.get_width()) // 8,
                                                    altura_mapa // 2 + 100))
        tela_pausa.blit(carta_sec_redimensionada, ((largura_mapa - carta_sec_redimensionada.get_width()) // 1.5,
                                                    altura_mapa // 2 + 100))
        
       
        ################################################################################################################################

        pygame.display.flip()
        # Certifique-se de ajustar a taxa de atualização da tela
        pygame.time.delay(30)  # Introduz um pequeno atraso para controlar a taxa de atualização
        print(velocidade_personagem)
    return velocidade_personagem
    # Retornar ao jogo
    pygame.display.set_mode((largura_tela, altura_tela))


