# SetGame
An algorithm that uses OpenCV to solve a game of Set (https://www.gigamic.com/jeu/set). create_image.py allows the user to manually select the cards on a picture of
the game (such as test_complet0.png) and saves each of the 12 cards in the folder. After that, pic_rec.py opens those images and, for each card, finds :
- the color of the symbole
- their shape
- their filling
- their number

Based on that, it indicates if at least one solution to the game exists, and if the answer is yes, which ones.
