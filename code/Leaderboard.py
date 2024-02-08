import sqlite3
import pygame

# Connect to the SQL database for leaderboard
leaderboard_conn = sqlite3.connect('leaderboard.db')
leaderboard_c = leaderboard_conn.cursor()

# Create a table for the leaderboard if it doesn't already exist
leaderboard_conn.execute('''CREATE TABLE IF NOT EXISTS leaderboard
             (username TEXT, score INT)''')

# Query the database to retrieve the top scores
top_scores = leaderboard_conn.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 10").fetchall()

# Create a Pygame window to display the leaderboard
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Leaderboard')

# Draw the leaderboard on the Pygame window
font = pygame.font.Font(None, 36)
y = 50
for row in top_scores:
    name = row[0]
    score = row[1]
    text = font.render(f'{name}: {score}', True, (255, 255, 255))
    screen.blit(text, (100, y))
    y += 50

# Display the Pygame window until the user closes it
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

# Close the SQL database connection when the program is done
leaderboard_conn.close()
