# if23_projet2024

Ce projet a pour but de déterminer la zone dans laquelle on se trouve grâce à la force du signal wifi.
Attention : le code a été réalisé pour un chemin particulier donc ne pas oublier de modifier les chemins et le code est fait pour du windows.

Ordre des fichiers :

- sort_wifi_data.py
- get_formatted_data
- treat_data
- seach_new_data_area

Dans le fichier doc.json on stocke les dernières coordonnées de la salle.
Area 0 : C201;
Area 1 : C203;
Area 2 : C205;
Area 3 : C207;
Area 4 : C210;
Area 5 : C208;
Area 6 : C206;
Area 7 : C204;
Area 8-12 : 5 zones couloir B vers C

En commançant par le fichier sort_wifi_data.py, ce script permet d'enregistrer les données reçues des différents point wifi.

En utilisaent le script get_formatted_data on peut regrouper les fichiers en fichier csv ou en fichier json.

Le script treat_data permet de selection une valeur pour remplir les valeurs manquantes. Par exemple si on rentre 95, les valeurs manquantes vont être remplacer dans un dataframe par -95 et dans l'autre par la moyenne par position d'une même salle, et le reste par -95.

Le script search_new_data_area permet de detecter la zone actuelle. Pour cela il faut rentrer la valeur par laquelle on veut traiter les données manquantes (par exmple si on rentre 95, les données seront remplacées par -95). On a la possibilité de faire deux modes, soit en temps réel, soit données par données. Il va nous être renvoyé la zone dans laquelle on pense être. Remarque : si la valeur n'a pas été traité dans la partie précédente, le code ne vas pas s'exécuter.

