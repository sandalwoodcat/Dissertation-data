import gym
import pygame
import csv
import time


from gym.wrappers import Monitor
from pygame.locals import VIDEORESIZE


Participant_ID = 'test_1'
# environment names are Pong-v0, Breakout-v0, Tennis-v0,
env_name = 'Tennis-v0'




# Set up Gym environment and video
env = gym.make(env_name, difficulty=0)
env = Monitor(env, str(Participant_ID) + '/' + str(env_name), video_callable=lambda episode_id: True)
rendered = env.render(mode="rgb_array")
video_size = [rendered.shape[1], rendered.shape[0]]
fps = 8

# Set up Pygame
pygame.init()
screen = pygame.display.set_mode(video_size, pygame.RESIZABLE)
clock = pygame.time.Clock()


# Set up key mappings
pressed_keys = []
keys_to_action = env.get_keys_to_action()
relevant_keys = set(sum(map(list, keys_to_action.keys()), []))


# Set up CSV files
moves_file = open(str(Participant_ID) + '_' + str(env_name) + '_moves.csv', 'w', newline='')
moves_writer = csv.writer(moves_file)
moves_writer.writerow(['Game', 'Move'])
scores_file = open(str(Participant_ID) + '_' + str(env_name) + '_scores.csv', 'w', newline='')
scores_writer = csv.writer(scores_file)
scores_writer.writerow(['Game', 'Score', 'Time'])


# Set up video recording
video_num = 0


# Play for 10 minutes
start_time = time.time()
game_num = 1
game_score = 0
game_time = 0




while time.time() - start_time < 600:
   # Reset environment for new game
   obs = env.reset()
   done = False
   game_moves = []
   game_rewards = []


   # Play game
   while not done:
       # Display game screen
       screen.fill((0, 0, 0))
       pyg_img = pygame.surfarray.make_surface(obs.swapaxes(0, 1))
       pyg_img = pygame.transform.scale(pyg_img, video_size)
       screen.blit(pyg_img, (0, 0))
       pygame.display.update()
       clock.tick(fps)


       # Handle user input
       for event in pygame.event.get():
           # test events, set key states
           if event.type == pygame.KEYDOWN:
               if event.key in relevant_keys:
                   pressed_keys.append(event.key)
           elif event.type == pygame.KEYUP:
               if event.key in relevant_keys:
                   pressed_keys.remove(event.key)
           elif event.type == pygame.QUIT:
               running = False
           elif event.type == VIDEORESIZE:
               video_size = event.size
               screen = pygame.display.set_mode(video_size)
               print(video_size)


       pygame.display.flip()


       # Take action and record move
       action = keys_to_action.get(tuple(sorted(pressed_keys)), 0)
       obs, reward, done, info = env.step(action)


       game_rewards.append(reward)
       game_moves.append(action)
       game_score += reward
       game_time += 1


       if time.time() - start_time > 600 and game_num > 1:
           break


   # Record game data
   moves_writer.writerow([game_num, game_moves])
   moves_writer.writerow([game_num, game_rewards])
   scores_writer.writerow([game_num, game_score, game_time])


   # Reset game data for next game
   game_num += 1
   game_score = 0
   game_time = 0


# Close files
moves_file.close()
scores_file.close()


# Quit Pygame
pygame.quit()
