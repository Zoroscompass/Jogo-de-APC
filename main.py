import pygame
import sys
import random


pygame.init()
clock = pygame.time.Clock()


#variáveis:
tamanho=10
branco = (255, 255, 255)
preto = (0, 0, 0)
marrom=(150,75,0)
NomeJogo='Minecraft 2'
mensagem='Bem vindo, player. Pressione enter para continuar.'
escolha_menu='escolha uma opção:'
largura_game=135
altura_game=20
estado= 'INICIAL' #espécie de sinal que delimita cada área do projeto, como tela inical, menu, instruções e jogo
tela_game= pygame.display.set_mode((largura_game*tamanho,altura_game*tamanho)) #display da tela do jogo
pontos=0 #contador dos pontos
contador_gasosa=400 #contador de combustível

#layout tela de início:
altura=600
largura= 900
tela_inicio= pygame.display.set_mode((largura,altura)) 

#Fontes
fonte_pri= pygame.font.SysFont('Arial',120)
fonte_sec= pygame.font.SysFont('Arial',20)
fonte_pri_menu= pygame.font.SysFont('Arial',30)
fonte_sec_menu= pygame.font.SysFont('Arial',20)
fonte_over1= pygame.font.SysFont('Arial',100)
fonte_over2= pygame.font.SysFont('Arial',20)

#Personagens:
cor_heroi=(0,255,0)
cor_inimigo=(255,0,0)
x=10
y=80
velocidade_heroi=5
inimigos= pygame.sprite.Group() #adiciona todas as classes para uma sprite, a fim de facilitar a manipulação conjunta das mesmas
rastros= pygame.sprite.Group() #idem
combustiveis= pygame.sprite.Group()#idem

#Disparos:
disparos=[] #inicializa a lista dos disparos que serão incluídos na sprite

#Classes:
class Heroi(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((12,12))
        self.image.fill(cor_heroi)
        self.rect= self.image.get_rect()
        self.rect.x= x
        self.rect.y= y
        self.velocidade= 5
        
    def update(self):
        contador_gasosa=400
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 30:
            self.rect.y -= self.velocidade
            contador_gasosa -= 2
        elif keys[pygame.K_s] and self.rect.y + 20 < altura_game * tamanho:
            self.rect.y += self.velocidade
            contador_gasosa -= 2
    

class Disparo(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((13,13))
        self.image.fill((47,79,47))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade= 10
    def tiro(self):
        self.rect.x += self.velocidade
        
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image= pygame.Surface((12,12))
        self.image.fill(cor_inimigo)
        self.rect= self.image.get_rect()
        self.rect.x= (largura_game * tamanho) - 20
        self.rect.y= random.randint(0,(altura_game*tamanho)-20)
        self.velocidade = 5
    def percurso(self):
        pygame.draw.rect(tela_game,branco,pygame.Rect(self.rect.x,self.rect.y,12,12))
        self.rect.x -= self.velocidade
    def volta_inicio(self):
        self.rect.x = (largura_game * tamanho) - 20
        self.rect.y = random.randint(0,(altura_game*tamanho)-20)

class Combustivel(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image= pygame.Surface((12,12))
        self.image.fill((0,0,255))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = 3
    
    def percurso_combustivel(self):
        pygame.draw.rect(tela_game,branco,pygame.Rect(self.rect.x,self.rect.y,12,12))
        self.rect.x -= self.velocidade
    
#Funções:
 
def primeira_tela(tela_inicio): #Função que cria a tela de boas vindas.
    titulo= fonte_pri.render(NomeJogo,True,marrom)
    subtitulo= fonte_sec.render(mensagem,True,branco)
    tela_inicio.fill(preto)
    tela_inicio.blit(titulo,(100,200))   
    tela_inicio.blit(subtitulo,(300,350))
    pygame.display.flip()
    
    
def menu(): # função que cria o menu.
    tela_inicio.fill(preto)
    titulo=fonte_pri.render(NomeJogo,True,marrom)
    texto_op=[
        '1- Jogar',
        '2- Configurações',
        '3- Ranking',
        '4- Instruções',
        '5- Sair'
    ]
    texto_op_rendered= [fonte_pri_menu.render(opcao,True,branco) for opcao in texto_op]
    
    tela_inicio.blit(titulo,(200,80))
    y_op= 210
    
    for texto_renderizado in texto_op_rendered:
        tela_inicio.blit(texto_renderizado,(370,y_op))
        y_op += 40
    
    pygame.display.flip()
    
    
def instrucoes(): #função que cria a tela de instruções
    tela_inicio.fill(preto)
    titulo = fonte_pri.render('Instruções', True, marrom)
    texto_instrucoes = [
        '1. Movimente-se  pressionando as teclas w e s.',
        '2. Dispare pressionando espaço.',
        '3. Jamais encoste nos inimigos vermelhos.',
        '4. Colete os personangens azuis, eles são o combustível.',
        '5. Derrote os inimigos para aumentar a pontuação.',
        '6. Cuidado!! O combustível reduz ao se movimentar e disparar.',
        '7. Nunca deixe o combustível chegar a 0.',
        '8. Pressione enter duas vezes para voltar ao menu.'
    ]
    texto_instrucoes_rendered = [fonte_pri_menu.render(instrucao, True, branco) for instrucao in texto_instrucoes]

    tela_inicio.blit(titulo, (200, 60))
    y_instrucao = 210
    
    for texto_renderizado in texto_instrucoes_rendered:
        tela_inicio.blit(texto_renderizado, (150, y_instrucao))
        y_instrucao += 30

    pygame.display.flip()
    reacao = True #Similar ao sinal do loop principal, mas verifica se o estado da tela de instrução ainda é válido.

    while reacao: #Loop que implementa a conexão entre a tela de instrução e a tela do menu.
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reacao = False


def tela_game_over(causa): #Função que cria a tela de game over de acordo com o tipo de morte.
    tela_game.fill(preto)  
    
    if causa == 'Inimigo':
        mensagem_morte= 'Player was blown up by enemy.'
    
    elif causa == 'Combustível':
        mensagem_morte= 'Player starved to death.'
    texto_game_over = fonte_over1.render('Game Over', True, (255,0,0))
    texto_pontuacao = fonte_over2.render(f'Pontuação: {pontos}', True, branco)
    texto_morte= fonte_over2.render(mensagem_morte,True,branco)

    tela_game.blit(texto_game_over, (largura_game * tamanho // 2 - 250, altura_game * tamanho // 2 - 100))
    tela_game.blit(texto_pontuacao, (largura_game * tamanho // 2 + 40, altura_game * tamanho // 2 + 8))
    tela_game.blit(texto_morte,(largura_game * tamanho // 2 - 220, altura_game * tamanho // 2 + 8))

    pygame.display.flip()
    
        
def atirar(): #Localiza o disparo para o centro do personagem e esconde seu rastro, além de adicionar para a sprite.
    disparo= Disparo(x + 7,y)
    disparos.append(disparo)
    esconde_tiro(disparo)
    todos_sprites.add(disparo)
    
def desenhar_disparos(tela_game):#layout do disparo
    for disparo in disparos:
        pygame.draw.rect(tela_game,(47,79,47),disparo.rect)

def esconde_tiro(disparo):#disfarça o rastro do personagem, ao fazer outro idêntico branco na posição anterior
    pygame.draw.rect(tela_game,branco,pygame.Rect(disparo.rect.x - 10, disparo.rect.y,20,20))  

def movimentacao_cima(): #movimentação para cima decrementando a velocidade
    global y
    y-=velocidade_heroi
    tela_heroi=pygame.draw.rect(tela_game,cor_heroi,pygame.Rect(x,y,12,12))

def movimentacao_baixo(): #movimentação para baixo incrementando a velocidade
    global y
    y+=velocidade_heroi
    tela_heroi=pygame.draw.rect(tela_game,cor_heroi,pygame.Rect(x,y,12,12))


def esconde_rastro(key):#função que esconde o rastro dependendo da direção da movimentação.
    global velocidade_heroi
    
    if key == 'w':
        rastro=pygame.draw.rect(tela_game,branco,pygame.Rect(x,(y+velocidade_heroi),12,12))
    else:
        rastro=pygame.draw.rect(tela_game,branco,pygame.Rect(x,(y-velocidade_heroi),12,12))
        
    return rastro
        
def surgimento_inimigo(): #função que atribuiu a classe Inimigo à variável inimigo e adiciona à sprite 
    inimigo= Inimigo()
    inimigos.add(inimigo)
    todos_sprites.add(inimigo)
        
def surgimento_combustivel():
    combustivel = Combustivel((largura_game * tamanho) - 20, random.randint(0, (altura_game * tamanho) - 20))
    combustiveis.add(combustivel)
    todos_sprites.add(combustivel)
        
primeira_tela(tela_inicio) 

heroi= Heroi(x,y)# equivalente a uma função surgimento_herói
todos_sprites= pygame.sprite.Group()
todos_sprites.add(heroi)
    
#Loop principal:
sinal = True
tecla_espaco= False
causa= None

while sinal:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sinal = False

        elif event.type == pygame.KEYDOWN: # O sinal deixa de ser verdadeiro para a tela de início e passa a ser para o menu.
            if estado == "INICIAL" and event.key == pygame.K_RETURN:
                estado = "MENU"
                menu()

            elif estado == "MENU": #configura os caminhos de acordo com a escolha do jogador
                if event.key == pygame.K_5:
                    sinal = False
                
                elif event.key == pygame.K_4:
                    estado = 'INSTRUCAO'
                    instrucoes()
                    
                elif event.key == pygame.K_1:
                    estado = "JOGO"
                    tela_game = pygame.display.set_mode((largura_game * tamanho, altura_game * tamanho))
                    tela_game.fill(branco)
                
                elif estado == 'GAME OVER' and event.key == pygame.K_RETURN:
                    estado = 'MENU'
                    menu()
                    
    if estado == 'INSTRUCAO':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sinal = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    estado = "MENU"
                    menu()
            
    elif estado == "JOGO":
        keys = pygame.key.get_pressed()

        if random.randint(0, 100) < 10: #configura o surgimento dos inimigos com um algoritmo randomico.
            surgimento_inimigo()
            
        if random.randint(0,100) < 5: #idem
            surgimento_combustivel()

        for inimigo in inimigos:#configura o movimento de cada disparo dentro da lista
            inimigo.percurso()
            pygame.draw.rect(tela_game, cor_inimigo, inimigo.rect)
            
            if pygame.sprite.spritecollide(heroi, inimigos,True): #função que verifica colisão entre as classes Heroi e Inimigo
                estado='GAME OVER'
                causa= 'Inimigo'
        
        if contador_gasosa <=0:
            estado='GAME OVER'
            causa='Combustível'
            
        if keys[pygame.K_w] and y > 30: #configura a movimentação para cima e seu limite
            movimentacao_cima()
            esconde_rastro('w')
            movimentacao_cima()
            contador_gasosa -= 2

        elif keys[pygame.K_s] and y + 20 < altura_game * tamanho: #configura a movimentação para baixo e seu limite
            movimentacao_baixo()
            esconde_rastro('s')
            movimentacao_baixo()
            contador_gasosa -= 2

        elif keys[pygame.K_SPACE] and not tecla_espaco: #gera os disparos a cada vez que o espaço for pressionado
            atirar()
            contador_gasosa -= 3
            tecla_espaco = True

        elif not keys[pygame.K_SPACE]:
            tecla_espaco = False
        
        
        for disparo in disparos:
            disparo.tiro()
            esconde_tiro(disparo)
            colisoes = pygame.sprite.spritecollide(disparo, inimigos, True) #verifica a colisão entre o grupo de sprites do inimigo e o heroi, removendo o inimigo quando este acertar o heroi

            for inimigo in colisoes:
                inimigo.kill()
                pontos += 50

        for combustivel in combustiveis.copy(): #cria um grupo de sprites para o combustível e itera cada um
            combustivel.percurso_combustivel()
            pygame.draw.rect(tela_game, (0, 0, 255), combustivel.rect)

            if pygame.sprite.spritecollide(heroi,combustiveis, True): #mesma lógica dos inimigos
                contador_gasosa += 40

    
        inimigos.update()
        combustiveis.update()
        heroi.update()
        
        pygame.draw.rect(tela_game, preto, (0, 0, largura_game * tamanho, 30))
        fonte_pontos = pygame.font.SysFont('Arial', 20)
        texto_pontos = fonte_pontos.render(f'Pontos: {pontos}', True, branco)
        tela_game.blit(texto_pontos, (10, 6))

        fonte_gasosa = pygame.font.SysFont('Arial', 20)
        texto_gasosa = fonte_gasosa.render(f'Combustível: {int(contador_gasosa)}', True, branco)
        tela_game.blit(texto_gasosa, (115 * tamanho, 6))

        desenhar_disparos(tela_game)
        todos_sprites.update()

        pygame.draw.rect(tela_game, cor_heroi, pygame.Rect(x, y, 12, 12))
        pygame.display.flip()
        contador_gasosa -= 1
        clock.tick(20)

    elif estado == 'GAME OVER':
        tela_game_over(causa)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sinal = False
            
                    
                    
        
pygame.quit()
sys.exit()






