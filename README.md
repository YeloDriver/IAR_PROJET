# les règles de notre robot
- il permet seulement de 4 actions, aller vers haut(0), vers droite(1), vers bas(2), vers gauche(3) et il ne permet pas de passage en diagonale pour ne pas laisser des endroits parcourus mais non balayés
- la consommation de la batterie ne correspond pas à l'action mais seulement au temps et le temps pour une action coûte 1 batterie
- les murs et les frontières ne peuvent pas être franchis
- les carreaux de la carte a trois états: 0 pour ceux non balayés, 1 pour ceux balayés, 3 pour les mur (2 pour présenter le robot sur la carte, mais c'était seulement utilisé dans la fonction de montrer des traces)
- pour le reward, dans le cas de ql, R(s) peut avoir plusieurs valeurs selon la trace du coup le coefficient gamma pour max(q(s',a')) devait être très bas
- pour l'entraînement plus rapide, nous avons utilisé le nombre d'épisode constant au lieu d'entraînement jusqu'à la convergence
  

# les règles de reward
- marcher sur un carreau non balayé : +5
- marcher sur un carreau balayé : +0
- battery==0 : +0 et arrêter 
- la carte est tout balayé : +100
- les actions ou les états impossibles : -1000

# les états utilisés dans notre algorithme
[robot.posX,robot.posY,robot.battery,robot.last_action]

# les auteurs des algorithmes
- q learning et monte carlo sont écrits par Jicheng Zhao (jicheng.zhao@insa-lyon.fr)
- dynamic programming est écrit par Hui Huang (hui.huang@insa-lyon.fr)
- si vous avez des questions concernants les algorithmes, n'hésitez pas à nous écrire pour demander

# la présentation des fichiers
- robot.py : il y a des structures des robots et des cartes dedans, y compris leurs règles de mouvement
- simulator.py : ce sont des règles de reward pour les états et les actions
- dp.py : le fichier de l'algorithme 'Dynamic Programming', il permet de s'exécuter tout seul
- ql.py : le fichier de l'algorithme 'q learning', il permet de s'exécuter tout seul
- mc.py : le fichier de l'algorithme 'Monte Carlo', il permet de s'exécuter tout seul
- main.py : le fichier qui permet de présenter tous les trois algorithmes and you can choose to see the trace with the algorithme or not
- ## l'exécution : python main.py

# les problèmes de notre projet
1. Nous n'arrivons pas trouvé un bon état pour exprimer la trace dans les tableaux (Nous avons testé beaucoup de paramètres mais aucun ne marche mieux que celui là). Notre trace n'a pas une bonne performance avec un entraînement non assez
2. Il faut trop d'entraînement pour arriver à la convergence de q table et ça coûte trop longtemps
