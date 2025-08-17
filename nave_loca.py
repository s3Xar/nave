import pygame
import math

pygame.init()

sw = 1000
sh = 1000
clock = pygame.time.Clock()
black = (0, 0, 0)
yellow = (255, 212, 59)
red = (255, 0, 0)


screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption('nave_prueba_2')

class Ship:
    def __init__(self, x, y, speed):
        self.position = pygame.math.Vector2(x, y)
        self.angle = 0
        self.direction = pygame.math.Vector2(0, 1) #definir la dirección incial que tiene el sprite dependiendo de la orientación del png
        self.speed = speed
        self.img_ship = pygame.image.load('nave/spr_nave.png')
        self.img_ship_size = self.img_ship.get_size() #al sacar el tamaño del sprite podemos definir dónde se ubica el punto de donde debe partir la bala
        self.point_head = pygame.Vector2((self.position[0] + (self.img_ship_size[0]//2)), self.position[1]) #para ubicar el punto de origen de la bala
        self.trans_point_head = self.point_head - self.position #devuelve el punto a la posición correcta


    def rotate_ship(self):
        self.rect_img_ship = self.img_ship.get_rect(center = self.position)
        self.mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        self.d_m_p = self.mouse_pos - self.position
        self.angle = math.atan2(self.d_m_p[1], self.d_m_p[0])
        self.img_rot_ship = pygame.transform.rotate(self.img_ship, - math.degrees(self.angle))
        self.rect_rot_ship = self.img_rot_ship.get_rect(center = (self.position))
        self.rot_direction_v= self.direction.rotate(math.degrees(self.angle) - 90) #difernciar las dos direcciones vertical y horizontal para que el moviemiento de la nave sea correcto
        self.rot_direction_h= self.direction.rotate(math.degrees(self.angle))
        self.rot_trans_point_head = self.trans_point_head.rotate(math.degrees(self.angle))
        self.rot_point_head = self.rot_trans_point_head + self.position
        

    def move_ship(self, dt):
        self.velocity_h = self.rot_direction_h * self.speed * dt
        self.velocity_v = self.rot_direction_v * self.speed * dt
        distance = self.d_m_p.length() #para que la nave no avance hasta más allá de la distancia del puntero del mouse
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and distance > 30 and keys[pygame.K_LSHIFT]:
            self.position += self.velocity_v * 3
        elif keys[pygame.K_w] and distance > 30:
            self.position += self.velocity_v
        if keys[pygame.K_s]:
            self.position -= self.velocity_v
        if keys[pygame.K_a]:
            self.position -= self.velocity_h
        if keys[pygame.K_d]:
            self.position += self.velocity_h
        

    def out_of_limits(self, screen):
       screen_rect = screen.get_rect()
       w, h = self.img_rot_ship.get_size()
       self.position.x = max(w/2, min(screen_rect.width - w/2, self.position.x))
       self.position.y = max(h/2, min(screen_rect.height - h/2, self.position.y))
        

    def update(self, dt):
       self.rotate_ship()
       self.move_ship(dt)
       self.out_of_limits(screen)
       screen.blit(self.img_rot_ship, self.rect_rot_ship)  

class Bullet:
    def __init__(self, origin, direction):
        self.origin = pygame.Vector2(origin)
        self.is_alive = True
        self.is_dead = False
        self.direction = pygame.Vector2(direction).normalize()
        self.lenght = 10
        self.speed = 800
        self.img_bullet = pygame.image.load('nave/spr_bullet.png')
        self.img_bullet = pygame.transform.rotozoom(self.img_bullet, 0, 2)
        dy, dx = self.direction.y, self.direction.x
        self.angle = -math.degrees(math.atan2(dy, dx)) + 90

    def draw(self):
        
        self.rot_img_bullet = pygame.transform.rotate(self.img_bullet, self.angle)
        self.rot_rect_img_bullet = self.rot_img_bullet.get_rect(center = self.origin)


    def move(self, dt):
        self.origin += self.direction * self.speed * dt

    def out_of_limits(self): #matar las balas cuando salgan de la pantalla
        if self.is_alive == True:
            pass
        else:
            pass
            

    def update(self, screen, dt):
        self.move(dt)
        self.draw()
        screen.blit(self.rot_img_bullet, self.rot_rect_img_bullet)

class Alien:
    def __init__():
        pass
        


Ship_1 = Ship(sw//2, sh//2, 200)
Bullets = []

running = True
while running:
    deltaTime = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                new_bullet = Bullet(Ship_1.rot_point_head, Ship_1.rot_direction_v)
                Bullets.append(new_bullet)
    

    screen.fill(black)
    Ship_1.update(deltaTime)
    # pygame.draw.rect(screen, yellow, Ship_1.rect_rot_ship, 1)

    for bullet in Bullets:
        bullet.update(screen, deltaTime)
        # pygame.draw.rect(screen, red, bullet.rot_rect_img_bullet, 1)
    
    

    pygame.display.flip()

pygame.quit()

