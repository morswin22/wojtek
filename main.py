import pygame
import tensorflow as tf
from tensorflow import keras

model = keras.models.load_model('model.h5')
model.summary()

pygame.font.init()
screen = pygame.display.set_mode((140,140))
font = pygame.font.SysFont('Comic Sans MS', 48)

draw_on = False
last_pos = (0, 0)
radius = 4

def roundline(surface, start, end, radius=1):
  dx = end[0]-start[0]
  dy = end[1]-start[1]
  distance = max(abs(dx), abs(dy))
  for i in range(distance):
    x = int(start[0] + float(i) / distance*dx)
    y = int(start[1] + float(i) / distance*dy)
    pygame.display.update(pygame.draw.circle(surface, (255, 255, 255), (x, y), radius))

while 1:
  e = pygame.event.wait()
  if e.type == pygame.QUIT:
    raise StopIteration
  if e.type == pygame.MOUSEBUTTONDOWN:
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (255, 255, 255), e.pos, radius)
    draw_on = True
  if e.type == pygame.MOUSEBUTTONUP:
    draw_on = False
    pxarray = pygame.PixelArray(pygame.transform.scale(screen, (28, 28)))
    data = []
    for y in range(pxarray.shape[0]):
      row = []
      for x in range(pxarray.shape[1]):
        row.append([pxarray[x, y] / 16777215])
      data.append(row)
    del pxarray
    tensor = tf.constant([data])
    prediction = model.predict(tensor)
    screen.fill((0,0,0))
    screen.blit(font.render(str(prediction[0].argmax()), False, (255, 255, 255)), (55,40))
  if e.type == pygame.MOUSEMOTION:
    if draw_on:
      pygame.display.update(pygame.draw.circle(screen, (255, 255, 255), e.pos, radius))
      roundline(screen, e.pos, last_pos,  radius)
    last_pos = e.pos
  pygame.display.flip()