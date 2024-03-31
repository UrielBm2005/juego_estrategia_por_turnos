import pygame
import sys, os
import random

# Inicializar Pygame
pygame.init()

# Configurar la ventana
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Catastrophy')
reloj = pygame.time.Clock()

# Configurar la cuadrícula
grid_size = 50
grid_rows = screen_height // grid_size
grid_columns = screen_width // grid_size
turno_jugador = True
jugador_ya_disparo = False

# Configurar el jugador y el enemigo
player_images = []
for i in range(5): # Asumiendo que hay 5 personajes
    image_path = f"assets//images//characters//player//player{i}.png"
    if os.path.exists(image_path):
        player_image = pygame.image.load(image_path)
        player_image = pygame.transform.scale(player_image, (50, 50)) # Escalar a 50x50 píxeles
        player_images.append(player_image)

for img in player_images:
    img = pygame.transform.scale(img, (50, 50))
enemy_image = pygame.image.load(f"assets//images//characters//enemigo//enemigo1.png")
enemy_image = pygame.transform.scale(enemy_image, (50, 50))

# Lista de jugadores con posiciones iniciales
jugadores = [
    {'x': 1, 'y': 0, 'image': player_images[0]},
    {'x': 1, 'y': 1, 'image': player_images[1]},
    {'x': 1, 'y': 2, 'image': player_images[2]},
    {'x': 1, 'y': 3, 'image': player_images[3]},
    {'x': 1, 'y': 4, 'image': player_images[4]}
]

def generate_random_position():
    x = random.randint(0, grid_columns - 1)
    y = random.randint(0, grid_rows - 1)
    return x, y

# Lista de enemigos con posiciones iniciales
enemigos = [
    {'x': 23, 'y': 0, 'image': player_images[0]},
    {'x': 23, 'y': 1, 'image': player_images[1]},
    {'x': 23, 'y': 2, 'image': player_images[2]},
    {'x': 23, 'y': 3, 'image': player_images[3]},
    {'x': 23, 'y': 4, 'image': player_images[4]}
]

# Índice del jugador actual
jugador_actual = 0

# Índice del enemigo actual
enemigo_actual = 0

def draw_grid():
    for row in range(grid_rows):
        for column in range(grid_columns):
            pygame.draw.rect(screen, (200, 200, 200), (column * grid_size, row * grid_size, grid_size, grid_size), 1)

# Cargar y escalar la imagen del arma y balas
weapon_image = pygame.image.load("assets//images//weapons//pistola0.png")
weapon_image = pygame.transform.scale(weapon_image, (10, 10)) # Asegúrate de escalar al tamaño correcto
imagen_balas = pygame.image.load(f"assets//images//weapons//bala_pistola.png")
imagen_balas = pygame.transform.scale(imagen_balas, (10, 10)) # Asegúrate de escalar al tamaño correcto

grupo_balas = pygame.sprite.Group()

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        super().__init__()
        self.image = imagen_balas
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direccion = direccion
        self.velocidad = 5 # Velocidad en píxeles por actualización
        self.distancia_restante = 100 # Distancia total a recorrer

    def update(self):
        if self.distancia_restante > 0:
            if self.direccion == 'UP':
                self.rect.y -= self.velocidad
            elif self.direccion == 'DOWN':
                self.rect.y += self.velocidad
            elif self.direccion == 'LEFT':
                self.rect.x -= self.velocidad
            elif self.direccion == 'RIGHT':
                self.rect.x += self.velocidad
            self.distancia_restante -= self.velocidad
        else:
            # Si la bala ha recorrido la distancia deseada, la eliminamos
            self.kill()

def draw_players():
    for jugador in jugadores:
        x, y = jugador['x'], jugador['y']
        screen.blit(jugador['image'], (x * grid_size, y * grid_size))
        weapon_x = x * grid_size + (grid_size + 40) // 2
        weapon_y = y * grid_size + (grid_size) // 2
        screen.blit(weapon_image, (weapon_x, weapon_y))

def draw_enemies():
    for enemy in enemigos:
        x, y = enemy['x'], enemy['y']
        inverted_image = pygame.transform.flip(enemy_image, True, False)
        screen.blit(inverted_image, (x * grid_size, y * grid_size))
        weapon_x = x * grid_size + (grid_size - 50) // 2
        weapon_y = y * grid_size + (grid_size) // 2
        inverted_weapon_image = pygame.transform.flip(weapon_image, True, False)
        screen.blit(inverted_weapon_image, (weapon_x, weapon_y))

def enemigo_disparar_bala(enemigo):
    x, y = enemigo['x'], enemigo['y']
    direccion = 'LEFT'
    bala = Bala(x * grid_size + grid_size // 2, y * grid_size, direccion)
    grupo_balas.add(bala)

def move_player(index, direction):
    global turno_jugador, jugador_ya_disparo
    if not turno_jugador: # Verificar si es el turno del jugador
        return # Si no es el turno del jugador, salir de la función
    jugador = jugadores[index]
    if direction == 'UP' and jugador['y'] > 0:
        jugador['y'] -= 1
    elif direction == 'DOWN' and jugador['y'] < grid_rows - 1:
        jugador['y'] += 1
    elif direction == 'LEFT' and jugador['x'] > 0:
        jugador['x'] -= 1
    elif direction == 'RIGHT' and jugador['x'] < grid_columns - 1:
        jugador['x'] += 1
    turno_jugador = False # Cambiar el turno al enemigo después de que el jugador se mueva
    jugador_ya_disparo = False # Permitir que el jugador dispare nuevamente

def move_enemy(index, direction):
    global turno_jugador
    if turno_jugador: # Verificar si es el turno del enemigo
        return # Si no es el turno del enemigo, salir de la función
    enemy = enemigos[index]
    if direction == 'UP' and enemy['y'] > 0:
        enemy['y'] -= 1
    elif direction == 'DOWN' and enemy['y'] < grid_rows - 1:
        enemy['y'] += 1
    elif direction == 'LEFT' and enemy['x'] > 0:
        enemy['x'] -= 1
    elif direction == 'RIGHT' and enemy['x'] < grid_columns - 1:
        enemy['x'] += 1
    turno_jugador = True # Cambiar el turno al jugador después de que el enemigo se mueva

def disparar_arma(jugador_actual):
    global jugador_ya_disparo
    if jugador_ya_disparo: # Verificar si el jugador ya ha disparado
        return # Si ya ha disparado, salir de la función
    jugador = jugadores[jugador_actual]
    direccion = 'RIGHT' # Asumiendo que el jugador dispara hacia la derecha
    bala = Bala(jugador['x'] * grid_size + grid_size // 2, jugador['y'] * grid_size, direccion)
    grupo_balas.add(bala)
    jugador_ya_disparo = True # Indicar que el jugador ya ha disparado

def check_collisions():
    global jugadores, enemigos
    for jugador in jugadores[:]: # Copia de la lista para no modificarla mientras se itera
        for enemy in enemigos[:]: # Lo mismo
            if jugador['x'] == enemy['x'] and jugador['y'] == enemy['y']:
                jugadores.remove(jugador)
                enemigos.remove(enemy)
                break # Salir del bucle interno después de encontrar una colisión

def game_loop():
    global turno_jugador, jugador_ya_disparo
    running = True
    while running:
        for         event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if turno_jugador: # Verificar si es el turno del jugador
                    if event.key == pygame.K_w:
                        move_player(jugador_actual, 'UP')
                    elif event.key == pygame.K_s:
                        move_player(jugador_actual, 'DOWN')
                    elif event.key == pygame.K_a:
                        move_player(jugador_actual, 'LEFT')
                    elif event.key == pygame.K_d:
                        move_player(jugador_actual, 'RIGHT')
                    elif event.key == pygame.K_SPACE and not jugador_ya_disparo: # Tecla para disparar
                        disparar_arma(jugador_actual)
                else: # Si es el turno del enemigo
                    if event.key == pygame.K_UP:
                        move_enemy(enemigo_actual, 'UP')
                    elif event.key == pygame.K_DOWN:
                        move_enemy(enemigo_actual, 'DOWN')
                    elif event.key == pygame.K_LEFT:
                        move_enemy(enemigo_actual, 'LEFT')
                    elif event.key == pygame.K_RIGHT:
                        move_enemy(enemigo_actual, 'RIGHT')

        fondo1 = pygame.image.load(f"assets//fondo.jpg")
        new_width = 1280 
        new_height = 720 
        scaled_background_image = pygame.transform.scale(fondo1, (new_width, new_height))
        reloj.tick(60)
        screen.blit(scaled_background_image,(0,0))
        draw_grid()

        # Actualizar y dibujar los jugadores
        draw_players()

        # Actualizar y dibujar los enemigos
        draw_enemies()

        # Actualizar y dibujar las balas
        grupo_balas.update()
        grupo_balas.draw(screen)

        # Verificar colisiones
        for bala in grupo_balas:
            for enemy in enemigos:
                if bala.rect.colliderect(enemy['x'] * grid_size, enemy['y'] * grid_size, grid_size, grid_size):
                    grupo_balas.remove(bala)
                    enemigos.remove(enemy)
                    break

        check_collisions()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

game_loop()

