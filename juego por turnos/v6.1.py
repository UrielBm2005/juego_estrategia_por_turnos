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
turno_enemigo = False
personaje_seleccionado = 0
mostrar_menu = False

# Variables para controlar el disparo
disparo_jugador = False
disparo_enemigo = False

# Cargar y escalar la imagen del arma y balas
arma_image = pygame.image.load("assets//images//weapons//pistola0.png")
arma_image = pygame.transform.scale(arma_image, (10, 10)) # Asegúrate de escalar al tamaño correcto
imagen_balas = pygame.image.load(f"assets//images//weapons//bala_pistola.png")
imagen_balas = pygame.transform.scale(imagen_balas, (10, 10)) # Asegúrate de escalar al tamaño correcto
grupo_balas = pygame.sprite.Group()

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion, propietario):
        super().__init__()
        self.image = imagen_balas
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direccion = direccion
        self.velocidad = 5 # Velocidad en píxeles por actualización
        self.distancia_restante = 100 # Distancia total a recorrer
        self.propietario = propietario # 'jugador' o 'enemigo'

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

# Configurar el jugador y el enemigo
player_images = []
for i in range(5): 
    image_path = f"assets//images//characters//player//player{i}.png"
    if os.path.exists(image_path):
        player_image = pygame.image.load(image_path)
        player_image = pygame.transform.scale(player_image, (50, 50)) # Escalar a 50x50 píxeles
        player_images.append(player_image)

for img in player_images:
    img = pygame.transform.scale(img, (50, 50))
enemy_image = pygame.image.load(f"assets//images//characters//enemigo//enemigo1.png")
enemy_image = pygame.transform.scale(enemy_image, (50, 50))

# Lista de jugadores con posiciones iniciales y armas
jugadores = [
    {'x': 1, 'y': 0, 'image': player_images[0], 'arma': arma_image, 'vida': 100},
    {'x': 1, 'y': 1, 'image': player_images[1], 'arma': arma_image, 'vida': 100},
    {'x': 1, 'y': 2, 'image': player_images[2], 'arma': arma_image, 'vida': 100},
    {'x': 1, 'y': 3, 'image': player_images[3], 'arma': arma_image, 'vida': 100},
    {'x': 1, 'y': 4, 'image': player_images[4], 'arma': arma_image, 'vida': 100}
]

# Lista de enemigos con posiciones iniciales
enemigos = [
    {'x': 23, 'y': 0, 'image': player_images[0], 'vida': 100},
    {'x': 23, 'y': 1, 'image': player_images[1], 'vida': 100},
    {'x': 23, 'y': 2, 'image': player_images[2], 'vida': 100},
    {'x': 23, 'y': 3, 'image': player_images[3], 'vida': 100},
    {'x': 23, 'y': 4, 'image': player_images[4], 'vida': 100}
]

def seleccionar_personaje(x, y):
    global personaje_seleccionado, disparo_jugador, disparo_enemigo
    for i, jugador in enumerate(jugadores):
        if jugador['x'] == x and jugador['y'] == y:
            personaje_seleccionado = i
            disparo_jugador = False # Resetear el estado de disparo del jugador
            disparo_enemigo = False # Resetear el estado de disparo del enemigo
            break

def mover_personaje(x, y):
    global turno_jugador, turno_enemigo, disparo_jugador, disparo_enemigo
    jugador = jugadores[personaje_seleccionado]
    if (abs(x - jugador['x']) <= 1 and abs(y - jugador['y']) <= 1 and
        x >= 0 and x < grid_columns and y >= 0 and y < grid_rows):
        jugador['x'] = x
        jugador['y'] = y
        turno_jugador = False
        turno_enemigo = True

def mover_enemigo():
    global turno_enemigo
    global turno_jugador

    enemigo = enemigos[0] # Asumiendo que solo hay un enemigo por ahora
    # Generar una nueva posición adyacente
    nueva_x = enemigo['x'] + random.randint(-1, 1)
    nueva_y = enemigo['y'] + random.randint(-1, 1)
    # Verificar si la nueva posición está dentro de los límites y es adyacente
    if (0 <= nueva_x < grid_columns and 0 <= nueva_y < grid_rows and
        abs(nueva_x - enemigo['x']) <= 1 and abs(nueva_y - enemigo['y']) <= 1):
        enemigo['x'] = nueva_x
        enemigo['y'] = nueva_y
    turno_enemigo = False
    turno_jugador = True

def dibujar_casillas_disponibles():
    jugador = jugadores[personaje_seleccionado]
    for i in range(jugador['x'] - 1, jugador['x'] + 2):
        for j in range(jugador['y'] - 1, jugador['y'] + 2):
            if 0 <= i < grid_columns and 0 <= j < grid_rows:
                pygame.draw.rect(screen, (100, 100, 100), (i * grid_size, j * grid_size, grid_size, grid_size), 1)

def draw_grid():
    for row in range(grid_rows):
        for column in range(grid_columns):
            pygame.draw.rect(screen, (200, 200, 200), (column * grid_size, row * grid_size, grid_size, grid_size), 1)

def draw_players():
    for jugador in jugadores:
        x, y = jugador['x'], jugador['y']
        screen.blit(jugador['image'], (x * grid_size, y * grid_size))
        # Dibujar el arma del personaje 100 píxeles en frente de él
        arma_x = x * grid_size + (grid_size - 50) // 2
        arma_y = y * grid_size + (grid_size) // 2
        screen.blit(jugador['arma'], (arma_x, arma_y))

def draw_enemies():
    for enemy in enemigos:
        x, y = enemy['x'], enemy['y']
        inverted_image = pygame.transform.flip(enemy_image, True, False)
        screen.blit(inverted_image, (x * grid_size, y * grid_size))
        weapon_x = x * grid_size + (grid_size - 50) // 2
        weapon_y = y * grid_size + (grid_size) // 2
        inverted_weapon_image = pygame.transform.flip(arma_image, True, False)
        screen.blit(inverted_weapon_image, (weapon_x, weapon_y))

def disparar_jugador(direccion):
    global disparo_jugador
    if disparo_jugador:
        return # No permitir disparar si ya se ha disparado en este turno
    jugador = jugadores[personaje_seleccionado]
    x_inicial = jugador['x'] * grid_size + (grid_size - 10) // 2
    y_inicial = jugador['y'] * grid_size
    if direccion == 'UP':
        bala = Bala(x_inicial, y_inicial, 'UP', 'jugador')
    elif direccion == 'DOWN':
        bala = Bala(x_inicial, y_inicial, 'DOWN', 'jugador')
    elif direccion == 'LEFT':
        bala = Bala(x_inicial, y_inicial, 'LEFT', 'jugador')
    elif direccion == 'RIGHT':
        bala = Bala(x_inicial, y_inicial, 'RIGHT', 'jugador')
    grupo_balas.add(bala)
    disparo_jugador = True # Marcar que el jugador ha disparado

def disparar_enemigo(direccion):
    global disparo_enemigo
    if disparo_enemigo:
        return # No permitir disparar si ya se ha disparado en este turno
    enemigo = enemigos[0] # Asumiendo que solo hay un enemigo por ahora
    x_inicial = enemigo['x'] * grid_size + (grid_size - 10) // 2
    y_inicial = enemigo['y'] * grid_size
    if direccion == 'UP':
        bala = Bala(x_inicial, y_inicial, 'UP', 'enemigo')
    elif direccion == 'DOWN':
        bala = Bala(x_inicial, y_inicial, 'DOWN', 'enemigo')
    elif direccion == 'LEFT':
        bala = Bala(x_inicial, y_inicial, 'LEFT', 'enemigo')
    elif direccion == 'RIGHT':
        bala = Bala(x_inicial, y_inicial, 'RIGHT', 'enemigo')
    grupo_balas.add(bala)
    disparo_enemigo = True # Marcar que el enemigo ha disparado

def resetear_disparos():
    global disparo_jugador, disparo_enemigo
    disparo_jugador = False
    disparo_enemigo = False

def check_collisions():
    """
    Verifica las colisiones entre jugadores y balas.
    Si una bala del enemigo toca a un jugador, se elimina el jugador.
    """
    global jugadores, enemigos
    # Crear listas temporales para almacenar los elementos a eliminar
    balas_a_eliminar = []
    jugadores_a_eliminar = []
    enemigos_a_eliminar = []

    # Iterar sobre las balas y jugadores para encontrar colisiones
    for bala in grupo_balas:
        # Verificar colisiones con jugadores
        for jugador in jugadores:
            if bala.rect.colliderect(jugador['x'] * grid_size, jugador['y'] * grid_size, grid_size, grid_size) and bala.propietario == 'enemigo':
                balas_a_eliminar.append(bala)
                jugadores_a_eliminar.append(jugador)
                break # Salir del bucle interno después de encontrar una colisión

        # Verificar colisiones con enemigos
        for enemigo in enemigos:
            if bala.rect.colliderect(enemigo['x'] * grid_size, enemigo['y'] * grid_size, grid_size, grid_size) and bala.propietario == 'jugador':
                balas_a_eliminar.append(bala)
                enemigos_a_eliminar.append(enemigo)
                break # Salir del bucle interno después de encontrar una colisión

    # Eliminar las balas, jugadores y enemigos marcados
    for bala in balas_a_eliminar:
        grupo_balas.remove(bala)
    for jugador in jugadores_a_eliminar:
        jugadores.remove(jugador)
    for enemigo in enemigos_a_eliminar:
        enemigos.remove(enemigo)

def dibujar_menu():
    # Dibujar el fondo del menú
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen_width, screen_height), 0)

    # Dibujar el botón para salir del juego
    pygame.draw.rect(screen, (255, 0, 0), (screen_width // 2 - 50, screen_height // 2 - 25, 100, 50), 0)
    texto_salir = font.render("Salir", True, (255, 255, 255))
    screen.blit(texto_salir, (screen_width // 2 - 40, screen_height // 2 - 15))

    # Dibujar el botón para regresar al juego
    pygame.draw.rect(screen, (0, 255, 0), (screen_width // 2 - 50, screen_height // 2 + 30, 100, 50), 0)
    texto_regresar = font.render("Regresar", True, (255, 255, 255))
    screen.blit(texto_regresar, (screen_width // 2 - 40, screen_height // 2 + 45))

def game_loop():
    global turno_jugador, turno_enemigo, personaje_seleccionado, mostrar_menu
    running = True
    mostrar_menu = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mostrar_menu = not mostrar_menu
                elif event.key == pygame.K_SPACE and mostrar_menu:
                    if mostrar_menu:
                        # Aquí puedes agregar la lógica para manejar las acciones de los botones del menú
                        pass
                elif not mostrar_menu:
                    # Aquí va el resto de la lógica del juego
                    pass

        if mostrar_menu:
            dibujar_menu()
        else:
            # Aquí va el resto de la lógica del juego
            pass
        
        # Actualizar las balas
        grupo_balas.update()

        # Verificar colisiones
        check_collisions()

        # Resetear disparos al final de cada turno
        if not turno_jugador:
            resetear_disparos()

        # Dibujar el fondo, la cuadrícula, los jugadores, las balas y los enemigos
        fondo1 = pygame.image.load(f"assets//fondo.jpg")
        new_width = 1280 
        new_height = 720 
        scaled_background_image = pygame.transform.scale(fondo1, (new_width, new_height))
        reloj.tick(60)
        screen.blit(scaled_background_image,(0,0))
        draw_grid()
        dibujar_casillas_disponibles()
        draw_players()

        # Dibujar las balas
        grupo_balas.draw(screen)

        # Actualizar y dibujar los enemigos
        draw_enemies()
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

game_loop()
