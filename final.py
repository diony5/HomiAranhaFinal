import pygame
from random import randint, choice
from pygame import display
from pygame.transform import scale
from pygame.image import load
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame import event
from pygame.locals import QUIT, KEYUP, K_SPACE
from pygame.time import Clock

pygame.init()
disparo = 0
tamanho = 800, 600  
superficie = display.set_mode((tamanho))  
display.set_caption('O  Homem Aranha')  

fundo = scale(load('images/cidade.jpg'),
              tamanho)  

class HomemAranha(Sprite):  
    def __init__(self, teia):
        super().__init__()  

        self.image = load('images/homemaranha_small.png')  
        self.rect = self.image.get_rect()  
        self.velocidade = 2
        self.teia = teia

    def update(self):

        keys = pygame.key.get_pressed() 

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade

    def soltarTeia(self):
        if len(self.teia) < 15:
            self.teia.add(
                Teia(*self.rect.center)
            )


class Teia(Sprite):  
    def __init__(self, x, y):
        super().__init__()

        self.image = load('images/teia_small.png')
        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self):
        self.rect.x += 1
        if self.rect.x > tamanho[0]:
            self.kill()


class Inimigo(Sprite): 
    def __init__(self):
        super().__init__()

        self.image = load('images/inimigo_1.png')
        self.rect = self.image.get_rect(
            center=(800, randint(10, 500))  
        )

    def update(self):
        self.rect.x -= 0.1


class Inimigo(Sprite):  
    def __init__(self):
        super().__init__()

        self.image = load('images/inimigo_1.png')
        self.rect = self.image.get_rect(
            center=(800, randint(10, 500)) 
        )

    def update(self):
        self.rect.x -= 1


class Chefao(Sprite):  
    def __init__(self):
        super().__init__()

        self.image = load('images/inimigo_2.png')
        self.rect = self.image.get_rect(
            center=(800, 300) 
        )

    def update(self):
        self.rect.x -= 0.1

grupo_inimigo = Group()
grupo_chefao = Group()
grupo_aranha = Group()
homem_aranha = HomemAranha(grupo_aranha)
grupo_geral = GroupSingle(homem_aranha)

grupo_inimigo.add(Inimigo())
grupo_chefao.add(Chefao())

round = 0
morte = 0
clock = Clock()

while True:

    clock.tick(120)
    if round % 120 == 0:
        grupo_inimigo.add(Inimigo())

    superficie.blit(fundo, (
        0, 0))  # Faço o Bit Blit na imagem no ponto 0,0 do plano definimo, com isso consigo inserir a imagem no jogo.
    grupo_geral.draw(superficie)  

    if (morte < 1):
        grupo_inimigo.draw(superficie)
        grupo_inimigo.update()
        disparo = 0
    else:
        grupo_chefao.draw(superficie)
        grupo_chefao.update()

    grupo_aranha.draw(superficie)

    grupo_geral.update()
    grupo_aranha.update()

    for evento in event.get(): 
        if evento.type == QUIT:
            pygame.quit()

        if evento.type == KEYUP:
            if evento.key == K_SPACE:
                homem_aranha.soltarTeia()


    if groupcollide(grupo_aranha, grupo_inimigo, True, True):
        morte += 1

    if disparo == 10:
        resposta = True
    else:
        resposta = False

    if groupcollide(grupo_aranha, grupo_chefao, True, resposta):
        disparo += 1

    round += 1
    display.update()  # a função update atualiza os frames.
