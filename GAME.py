
import pygame
import sys
import random
import math
from Tela_Cartas import tela_de_pausa, velocidade_personagem,intervalo_disparo
from Variaveis import (largura_mapa, altura_mapa,largura_tela, altura_tela,LARGURA_CHEFE,ALTURA_CHEFE,vida_chefe,pos_x_chefe,pos_y_chefe,velocidade_chefe,projeteis_chefe,intervalo_projeteis,contagem_projeteis_chefe,max_projeteis_chefe,tamanho_projetil_chefe,chefe_atual,tempo_animacao_chefe,tempo_passado_chefe,vermelho,amarelo,pontuacao,
                 pontuacao_magia,altura_barra_vida,largura_barra_vida,vida,verde,vida_maxima,vel_inimig        )

# Inicializar o Pygame
pygame.init()

# Configurações do mapa
mapa_path = "Sprites/Mapa.png"

# Configurações do personagem
personagem_paths = {
    'up': ["Sprites/Geo.png", "Sprites/Geo2.png"],
    'down': ["Sprites/Geo.png", "Sprites/Geo2.png"],
    'left': ["Sprites/LadoE1.png", "Sprites/LadoE2.png"],
    'right': ["Sprites/LadoD1.png", "Sprites/LadoD2.png"],
    'stop': ["Sprites/Geo.png", "Sprites/Geo2.png"],
    'shift':["Sprites/LadoD1.png", "Sprites/LadoD2.png"]
}


frames_chefe = [pygame.transform.scale(pygame.image.load("Sprites/Boost.png"), (LARGURA_CHEFE, ALTURA_CHEFE)),
                 pygame.transform.scale(pygame.image.load("Sprites/Boost2.png"), (LARGURA_CHEFE, ALTURA_CHEFE))]

frames_inimigo = [pygame.transform.scale(pygame.image.load("Sprites/inimig.png"), (100, 100)),
                 pygame.transform.scale(pygame.image.load("Sprites/inimig2.png"), (102, 102))]

frames_inimigo2=[pygame.transform.scale(pygame.image.load("Sprites/inimig3.png"), (100, 100)),
                 pygame.transform.scale(pygame.image.load("Sprites/inimig4.png"), (102, 102))]

direcao_atual = 'stop'  # Direção inicial
largura_personagem, altura_personagem = 95, 95
pos_x_personagem, pos_y_personagem = 100, 100

tempo_animacao = 700  # Tempo em milissegundos entre cada quadro


relogio = pygame.time.Clock()
fps_alvo = 60  # Defina o número desejado de quadros por segundo
# Configurações do disparo
disparo_paths = ["Sprites/Fogo1.png", "Sprites/Fogo2.png"]
disparo_chefe=["Sprites/tiro.png", "Sprites/tiro2.png"]
largura_disparo, altura_disparo = 40, 40
velocidade_disparo = 10
disparos = []

# Configurações da tela

tela = pygame.display.set_mode((largura_tela, altura_tela),  pygame.FULLSCREEN)
pygame.display.set_caption("Renderizando Mapa com Personagem")

# Variáveis para a barra de magia
pontuacao_inimigos=0
maxima_pontuacao_magia = 750
piscar_magia = False


tempo_piscar_magia = 500  # Tempo em milissegundos para alternar entre visível e invisível
tempo_passado_piscar_magia = 0

#INIMIGOS
inimigos_eliminados = 0
tempo_ultimo_inimigo_apos_morte = pygame.time.get_ticks()
intervalo_geracao_inimigos_apos_morte = 7000  # Intervalo entre gerações em milissegundos
geracao_ativa_apos_morte = False

# Configurações do chefe
tempo_ultimo_disparo_chefe = pygame.time.get_ticks()

# Carregar a imagem do mapa
mapa = pygame.image.load(mapa_path).convert()
mapa = pygame.transform.scale(mapa, (largura_tela, altura_tela))

# Carregar as sequências de imagens do personagem
frames_animacao = {direcao: [pygame.image.load(path) for path in paths] for direcao, paths in personagem_paths.items()}
frames_animacao = {direcao: [pygame.transform.scale(frame, (largura_personagem, altura_personagem)) for frame in frames] for direcao, frames in frames_animacao.items()}

# Adicionar uma entrada para 'stop' no dicionário
frames_animacao['stop'] = [pygame.image.load(path) for path in personagem_paths['stop']]
frames_animacao['stop'] = [pygame.transform.scale(frame, (largura_personagem, altura_personagem)) for frame in frames_animacao['stop']]

# Carregar as sequências de imagens do disparo
frames_disparo = [pygame.image.load(path) for path in disparo_paths]
frames_disparo = [pygame.transform.scale(frame, (largura_disparo, altura_disparo)) for frame in frames_disparo]


#Carrega o disparo do BOSS
frame_projetil_chefe = [pygame.image.load(path) for path in disparo_chefe]
frame_projetil_chefe = [pygame.transform.scale(frame, (largura_disparo, altura_disparo)) for frame in frame_projetil_chefe]

# Configurações do loop principal
relogio = pygame.time.Clock()
tempo_passado = 0
frame_atual = 0
frame_atual_disparo = 0

# Atualizar a última direção da personagem
ultima_tecla_movimento = None
movimento_pressionado = False

#as seguintes variáveis para controle do tempo de hit do inimigo
tempo_ultimo_hit_inimigo = pygame.time.get_ticks()
intervalo_hit_inimigo = 400  # Intervalo de 1 segundo (ajuste conforme necessário)

# esta variável global para controlar o piscar da barra de vida
piscando_vida = False



def atualizar_posicao_personagem(keys):
    global pos_x_personagem, pos_y_personagem, direcao_atual, ultima_tecla_movimento
    global movimento_pressionado

    if keys[pygame.K_a]:
        pos_x_personagem = max(0, pos_x_personagem - velocidade_personagem)
        direcao_atual = 'left'
        ultima_tecla_movimento = 'left'
        movimento_pressionado = True
        print(velocidade_personagem)
    elif keys[pygame.K_d]:
        pos_x_personagem = min(largura_mapa - largura_personagem, pos_x_personagem + velocidade_personagem)
        direcao_atual = 'right'
        ultima_tecla_movimento = 'right'
        movimento_pressionado = True
    elif keys[pygame.K_w]:
        pos_y_personagem = max(0, pos_y_personagem - velocidade_personagem)
        direcao_atual = 'up'
        ultima_tecla_movimento = 'up'
        movimento_pressionado = True
    elif keys[pygame.K_s]:
        pos_y_personagem = min(altura_mapa - altura_personagem, pos_y_personagem + velocidade_personagem)
        direcao_atual = 'down'
        ultima_tecla_movimento = 'down'
        movimento_pressionado = True
    elif keys[pygame.K_LSHIFT]:
        pos_y_personagem = min(altura_mapa - altura_personagem, pos_y_personagem + 12)
        direcao_atual = 'shift'
        movimento_pressionado = True
    else:
        direcao_atual = 'stop'


tempo_ultimo_disparo_chefe = pygame.time.get_ticks()


# Antes do loop principal, crie uma lista para armazenar os inimigos
inimigos_comum = []
inimigos_chefe=[]
largura_inimigo, altura_inimigo = 120, 120

def criar_inimigo(x, y, tipo=1):
    if tipo == 1:
        image = pygame.transform.scale(pygame.image.load("Sprites/inimig.png"), (largura_inimigo, altura_inimigo))
    elif tipo == 2:
        print("inimigo 2")
        image = pygame.transform.scale(pygame.image.load("Sprites/inimig3.png"), (largura_inimigo, altura_inimigo))
    else:
        print("Inimigo")
        # Lidar com tipos desconhecidos ou erro de entrada
        image = pygame.transform.scale(pygame.image.load("Sprites/inimig.png"), (largura_inimigo, altura_inimigo))

    
    return {"rect": pygame.Rect(x, y, largura_inimigo, altura_inimigo), "image": image, "tipo": tipo}

def criar_chefe(x, y):
    return {
        "rect": pygame.Rect(x, y, LARGURA_CHEFE, ALTURA_CHEFE),
        "frames": [pygame.transform.scale(pygame.image.load("Sprites/Boost.png"), (LARGURA_CHEFE, ALTURA_CHEFE)),
                   pygame.transform.scale(pygame.image.load("Sprites/Boost2.png"), (LARGURA_CHEFE, ALTURA_CHEFE))],
        "atual": 0
    }

chefe_presente = False
chefe = criar_chefe(largura_tela - 600, 0)
    


# Configurações para controlar a criação de inimigos
dobro_pontuacao = 15  # Quantidade de pontos necessários para dobrar a pontuação e adicionar mais inimigos
pontuacao_dobro = dobro_pontuacao  # Inicializa a pontuação necessária para dobrar a pontuação

def verificar_colisao_disparo_inimigo(pos_disparo, pos_inimigo, largura_disparo, altura_disparo, largura_inimigo, altura_inimigo,inimigos_eliminados):
    rect_disparo = pygame.Rect(pos_disparo[0], pos_disparo[1], largura_disparo, altura_disparo)
    rect_inimigo = pygame.Rect(pos_inimigo[0], pos_inimigo[1], largura_inimigo, altura_inimigo)
    
    return rect_disparo.colliderect(rect_inimigo)

def verificar_colisao_disparo_chefe(pos_disparo, chefe, largura_disparo, altura_disparo):
    global vida_chefe
    global tempo_ultimo_inimigo_apos_morte
    global tempo_ultimo_inimigo
    rect_disparo = pygame.Rect(pos_disparo[0], pos_disparo[1], largura_disparo, altura_disparo)
    rect_chefe = chefe["rect"]

    if rect_disparo.colliderect(rect_chefe):
        # Remover disparo
        disparos.remove(pos_disparo)

        # Reduzir a vida do chefe
        vida_chefe -= 200  # Ajuste conforme necessário
        print("Estou morrendo")


        if vida_chefe <= 0:
            print("Chefe derrotado!")
            chefe_presente=False
            tempo_atual = pygame.time.get_ticks()

            if tempo_atual - tempo_ultimo_inimigo >= intervalo_geracao_inimigos_apos_morte:
                print("Vai gerar")
                for _ in range(5):  # Altere o número conforme necessário
                    print("Gerou 5")
                    inimigos_comum.append(criar_inimigo(largura_mapa, random.randint(10, altura_mapa), tipo=2))  # Adicionar mais inimigos
                tempo_ultimo_inimigo_apos_morte = tempo_atual  # Atualizar o tempo do último inimigo adicionado
                
        return True  # Indica que houve colisão

    return False  # Indica que não houve colisão

# Variável para armazenar o tempo do último inimigo adicionado
tempo_ultimo_inimigo = pygame.time.get_ticks()
quantidade_inimigos = 1

# Função para verificar a colisão entre o personagem e os projéteis inimigos
def verificar_colisao_personagem(projeteis):
    global pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem

    for proj in projeteis:
        pos_x_proj, pos_y_proj = proj["rect"].x, proj["rect"].y

        if (
            pos_x_personagem < pos_x_proj < pos_x_personagem + largura_personagem and
            pos_y_personagem < pos_y_proj < pos_y_personagem + altura_personagem
        ):
            return True  # Colisão detectada

    return False  # Sem colisão

def verificar_colisao_personagem_inimigo(personagem_rect, inimigos_rects):
    tempo_atual = pygame.time.get_ticks()
    for inimigo_rect in inimigos_rects:
        if personagem_rect.colliderect(inimigo_rect):
            return True  # Colisão detectada

    return False  # Sem colisão


# Variáveis para a animação da flor
animacao_flor = False
tempo_animacao_flor = 2000  # Tempo em milissegundos para a animação da flor
tempo_passado_animacao_flor = 0

tempo_ultimo_disparo = pygame.time.get_ticks()


###################################################################################################PRINCIPAL#################################################################################################################
#LOOP PRINCIPAL
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()

    atualizar_posicao_personagem(keys)

    

    novos_inimigos = []
    novos_disparos = []
    inimig_atin=[]

    for inimigo in inimigos_comum:
        inimigo_rect = inimigo["rect"]
        inimigo_image = inimigo["image"]

        inimigo_atingido = False

        for disparo in disparos:
            
            if verificar_colisao_disparo_inimigo(disparo, (inimigo["rect"].x, inimigo["rect"].y), largura_disparo, altura_disparo, largura_inimigo, altura_inimigo,inimigos_eliminados):
                print("Colisão detectada! Removendo disparo e inimigo.")
                print(f"Posição do inimigo: {inimigo_rect.x}, {inimigo_rect.y}")
                print(f"Posição do disparo: {disparo[0]}, {disparo[1]}")
                # Remover disparo
                disparos.remove(disparo)
                inimigo_atingido = True
                print("Disparo removido.")

                inimigos_comum.remove(inimigo)
                inimigos_eliminados += 1

                pontuacao += 750
                pontuacao_inimigos += 1
                # Verificar se a pontuação atingiu o dobro
                if pontuacao >= pontuacao_dobro:
                    pontuacao_dobro += dobro_pontuacao  # Ajustar a próxima pontuação necessária para dobrar
                    if inimigos_eliminados >=5:
                        inimigos_eliminados=0
                        for _ in range(3):
                            inimigos_comum.append(criar_inimigo(largura_mapa, random.randint(10, altura_mapa)))  # Adicionar mais inimigos
                    break  # Sair do loop ao encontrar uma colisão
        if inimigo_atingido:
            break  # Sair do loop externo se um inimigo foi atingido
    

    
        if pontuacao > pontuacao_magia:
            pontuacao_magia = min(pontuacao, maxima_pontuacao_magia)

        

    def criar_disparo():
        return {"rect": pygame.Rect(pos_x_personagem, pos_y_personagem, largura_disparo, altura_disparo),"direcao": ultima_tecla_movimento }

    # Adicionar um novo disparo quando a tecla de espaço é pressionada
    tempo_atual = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and movimento_pressionado and tempo_atual - tempo_ultimo_disparo >= intervalo_disparo:
        
        if ultima_tecla_movimento is not None:
            print(ultima_tecla_movimento)
            pos_x_disparo = pos_x_personagem + largura_personagem // 1 - largura_disparo // 1
            pos_y_disparo = pos_y_personagem + altura_personagem // 1 - altura_disparo // 1
            disparos.append((pos_x_disparo, pos_y_disparo, ultima_tecla_movimento ))
            tempo_ultimo_disparo = tempo_atual  # Atualizar o tempo do último disparo

    tempo_passado += relogio.get_rawtime()
    relogio.tick()

     # Adicionar inimigos a cada 10 segundos
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - tempo_ultimo_inimigo >= 4000:  # 10000 milissegundos = 10 segundos
        if not chefe_presente:
            (inimigos_comum.append(criar_inimigo(largura_mapa, random.randint(10, altura_mapa))))  # Adicionar mais inimigos
            tempo_ultimo_inimigo = tempo_atual  # Atualizar o tempo do último inimigo adicionado
    if pontuacao_inimigos >= 3000 * quantidade_inimigos:
        quantidade_inimigos += 1
        print("Parece que a dificuldade aumentou")
        

    if tempo_passado >= tempo_animacao:
        tempo_passado = 0
        frame_atual = (frame_atual + 1) % len(frames_animacao[direcao_atual])

    tela.fill((255, 255, 255))
    tela.blit(mapa, (0, 0))
    tela.blit(frames_animacao[direcao_atual][frame_atual], (pos_x_personagem, pos_y_personagem))

    

    
    # Desenhar os disparos normais
    novos_disparos = []
    for disparo in disparos:
        pos_x_disparo, pos_y_disparo, direcao_disparo = disparo
        tela.blit(frames_disparo[frame_atual_disparo], (pos_x_disparo, pos_y_disparo))

        # Atualizar a posição do disparo
        if direcao_disparo == 'up':
            pos_y_disparo -= velocidade_disparo
        elif direcao_disparo == 'down':
            pos_y_disparo += velocidade_disparo
        elif direcao_disparo == 'left':
            pos_x_disparo -= velocidade_disparo
        elif direcao_disparo == 'right':
            pos_x_disparo += velocidade_disparo

        # Adicionar o disparo à lista se não atingir o final do mapa
        if (
            0 <= pos_x_disparo < largura_mapa and
            0 <= pos_y_disparo < altura_mapa
        ):
            novos_disparos.append((pos_x_disparo, pos_y_disparo, direcao_disparo))

    disparos = novos_disparos

    frame_atual_disparo = (frame_atual_disparo + 1) % len(frames_disparo)

    

    for inimigo in inimigos_comum:
        dx = pos_x_personagem - inimigo["rect"].x
        dy = pos_y_personagem - inimigo["rect"].y
        dist = max(40, abs(dx) + abs(dy))
        inimigo["rect"].x += (dx / dist) * vel_inimig
        inimigo["rect"].y += (dy / dist) * vel_inimig
        for inimigo in inimigos_comum:
            if inimigo["tipo"] == 2:  # Verifica se é do tipo 2
                inimigo["image"] = frames_inimigo2[frame_atual % len(frames_inimigo2)]
            else:
                inimigo["image"] = frames_inimigo[frame_atual % len(frames_inimigo)]

            tela.blit(inimigo["image"], inimigo["rect"].topleft)
    

    # Após verificar o número de inimigos eliminados
    if pontuacao_inimigos >= 75 and vida_chefe > 0:
        chefe_presente= True
        inimigos_chefe.append(criar_chefe(largura_tela - 600 , 0))

        if chefe_presente:
            pos_chefe = (chefe["rect"].x, chefe["rect"].y)
            pos_x_chefe -= velocidade_chefe
            chefe["image"] = frames_chefe[frame_atual % len(frames_chefe)]
            tela.blit(chefe["image"], chefe["rect"].topleft)

            inimigos_comum=[]
            # Desenhar a barra de vida do Chefe
            cor_vida_chefe = (255, 0, 0)  # Vermelho
            largura_barra_vida_chefe = (vida_chefe / 1500) * largura_mapa
            pygame.draw.rect(tela, cor_vida_chefe, (0, 0, largura_barra_vida_chefe, 20))

            fonte_barra_vida = pygame.font.Font(None, 36)
            texto_barra_vida = fonte_barra_vida.render(f'{vida_chefe}/{1500}', True, (255, 255, 255))
            tela.blit(texto_barra_vida, (largura_mapa - 960, 0))

            for proj in projeteis_chefe:
                pos_x_proj, pos_y_proj = proj["rect"].x, proj["rect"].y
                tela.blit(frame_projetil_chefe[frame_atual_disparo], (pos_x_proj, pos_y_proj))

            for disparo in disparos:
                if verificar_colisao_disparo_chefe(disparo, chefe, largura_disparo, altura_disparo):
                    
                    pass

            # Verificar a colisão entre o personagem e os projéteis inimigos
            if verificar_colisao_personagem(projeteis_chefe):
                print("Você foi atingido! Fim de jogo.")
                running = False  # Encerrar o jogo

    if vida_chefe <= 0:
        tempo_atual = pygame.time.get_ticks()

        if tempo_atual - tempo_ultimo_inimigo_apos_morte >= intervalo_geracao_inimigos_apos_morte:
            for _ in range(3):
                inimigos_comum.append(criar_inimigo(largura_mapa, random.randint(10, altura_mapa), tipo=2))
            tempo_ultimo_inimigo_apos_morte = tempo_atual  # Atualizar o tempo do último inimigo adicionado
    personagem_rect = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)
    inimigos_rects = [inimigo["rect"] for inimigo in inimigos_comum]

    if verificar_colisao_personagem_inimigo(personagem_rect, inimigos_rects):
        print("Meu Deus, ele me tocou!!!")
        
        if tempo_atual - tempo_ultimo_hit_inimigo >= intervalo_hit_inimigo:
            vida -= 25
            tempo_ultimo_hit_inimigo = tempo_atual  # Atualize o tempo do último hit do inimigo
            # esta parte para iniciar o piscar da barra de vida
            piscando_vida = True
        
    if vida <=0:
        running=False

    # Adicione esta verificação para controlar o piscar da barra de vida
    if piscando_vida:
        if tempo_atual % 500 < 250:  # Altere o valor 500 e 250 conforme necessário
            # Desenha a barra de vida piscando em vermelho
            pygame.draw.rect(tela, (255, 0, 0), (posicao_barra_vida[0], posicao_barra_vida[1], largura_barra_vida, altura_barra_vida))
        else:
            # Desenha a barra de vida normalmente
            pygame.draw.rect(tela, verde, (posicao_barra_vida[0], posicao_barra_vida[1], (vida / 250) * largura_barra_vida, altura_barra_vida))

        # Adicione esta verificação para parar o piscar depois de um tempo
        if tempo_atual - tempo_ultimo_hit_inimigo >= intervalo_hit_inimigo:
            piscando_vida = False

    tempo_atual = pygame.time.get_ticks()

    if tempo_atual - tempo_ultimo_disparo_chefe >= intervalo_projeteis:
        if contagem_projeteis_chefe < max_projeteis_chefe:
            # Adicione um novo projétil à lista de projéteis do chefe
            pos_x_proj = largura_tela - LARGURA_CHEFE // 2
            pos_y_proj = random.randint(0, 980 - altura_disparo)
            projeteis_chefe.append({"rect": pygame.Rect(pos_x_proj, pos_y_proj, tamanho_projetil_chefe, tamanho_projetil_chefe),
                                "direcao": "left"})
            tempo_ultimo_disparo_chefe = tempo_atual
            contagem_projeteis_chefe += 1
    else:
        # Resetar a contagem após atingir o número máximo de projéteis
        contagem_projeteis_chefe = 0



    # Mova os projéteis do chefe e verifique colisões
    novos_projeteis_chefe = []
    for proj in projeteis_chefe:
        pos_x_proj, pos_y_proj, direcao_proj = proj["rect"].x, proj["rect"].y, proj["direcao"]
    
        # Mova o projétil na direção correta
        if direcao_proj == 'left':
            pos_x_proj -= velocidade_disparo
    
        # Adicione o projétil de volta à lista se não atingir o final do mapa
        if 0 <= pos_y_proj < altura_mapa:
            novos_projeteis_chefe.append({"rect": pygame.Rect(pos_x_proj, pos_y_proj, largura_disparo, altura_disparo),
                                      "direcao": direcao_proj})

    projeteis_chefe = novos_projeteis_chefe
        

    

    
    # Desenha a barra de magia
    
    largura_barra_magia = (pontuacao_magia / maxima_pontuacao_magia) * 750  # Ajuste conforme necessário
    pygame.draw.rect(tela, (53,239,252), (1, 59, largura_barra_magia, 25))

    # Desenha a  pontos
    fonte = pygame.font.Font(None, 26)
    texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, (0, 0, 0))
    tela.blit(texto_pontuacao, (10, 61.8))
    # Verifica se a pontuação da magia atingiu o máximo para iniciar a animação da flor
    if pontuacao_magia == maxima_pontuacao_magia and not animacao_flor:

        animacao_flor = True
        tempo_passado_animacao_flor = 0

    # Animação da flor
    if animacao_flor:
        tempo_passado_animacao_flor += relogio.get_rawtime()
        if tempo_passado_animacao_flor <= tempo_animacao_flor:
            # Diminui a barra de magia
            largura_barra_magia -= (relogio.get_rawtime() / tempo_animacao_flor) * 20

            # Desenha a flor giratória
            centro_flor = (20 + largura_barra_magia, 70)
            raio_flor = 20
            petalas = 5
            angulo_inicial = (tempo_passado_animacao_flor / tempo_animacao_flor) * 360
            for i in range(petalas):
                angulo = angulo_inicial + (i * (360 / petalas))
                x_petalas = centro_flor[0] + raio_flor * math.cos(math.radians(angulo))
                y_petalas = centro_flor[1] + raio_flor * math.sin(math.radians(angulo))
                pygame.draw.circle(tela, (53,239,252), (int(x_petalas), int(y_petalas)), 13)
        else:
            animacao_flor = False 
    # Verifica se a pontuação atingiu 1500 e se o jogador pressionou 'Q'
    if pontuacao >= 750 and keys[pygame.K_q]:
        pontuacao-=750
        pontuacao_magia-=750
        animacao_flor=False
        print("Escolha seus atributos")
        tela_de_pausa()

    relogio.tick(fps_alvo)
    posicao_barra_vida = (largura_tela // 2.73 - largura_barra_vida // 1, altura_tela - (altura_tela-30))
    pygame.draw.rect(tela, verde, (posicao_barra_vida[0], posicao_barra_vida[1], (vida / 250) * largura_barra_vida, altura_barra_vida))
    pygame.draw.rect(tela, (255, 255, 255), (posicao_barra_vida[0], posicao_barra_vida[1], largura_barra_vida, altura_barra_vida), 2)
    # Desenha a quantidade total de vida e a vida atual sobre a barra
    fonte_vida = pygame.font.Font(None, 24)
    texto_vida = fonte_vida.render(f'Vida: {vida}/{vida_maxima}', True, (0, 0, 0))
    tela.blit(texto_vida, (largura_tela // 2.73 - largura_barra_vida // 1.5, altura_tela - (altura_tela-33)))

    pygame.display.flip()


# Encerrar o Pygame
pygame.quit()
sys.exit()