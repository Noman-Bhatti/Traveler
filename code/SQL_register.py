import pygame
import sqlite3
from Sprites import *
from settings import *

pygame.init()
screen = pygame.display.set_mode((500, 300))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

# Create a connection to the database
conn = sqlite3.connect('users.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT, password TEXT, score INTEGER)''')
# Add rows of data
c.execute("INSERT INTO users (username, password) VALUES ('admin', 'password')")


conn.commit()

class TextBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event, Text_boxes):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the Text_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the Text box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Insert username and password into the database
                    c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                              (Text_boxes[0].text, Text_boxes[1].text))

                    # Commit the changes made to the database
                    conn.commit()

                    print("Registration successful!")
                    Text_boxes[0].text = ''
                    Text_boxes[1].text = ''
                    # Re-render the text.
                    Text_boxes[0].txt_surface = FONT.render(Text_boxes[0].text, True, self.color)
                    Text_boxes[1].txt_surface = FONT.render(Text_boxes[1].text, True, self.color)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

def registration():
    text = FONT.render('Register', True, WHITE)
    text_rect = text.get_rect(center=(100, 70))
    clock = pygame.time.Clock()
    Text_box1 = TextBox(100, 150, 140, 32)
    Text_box2 = TextBox(100, 200, 140, 32)
    Text_boxes = [Text_box1, Text_box2]
    done = False

    while not done:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True
            for box in Text_boxes:
                box.handle_event(event, Text_boxes)

        for box in Text_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in Text_boxes:
            box.draw(screen)

        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(30)
    # Close connection
    conn.close()
