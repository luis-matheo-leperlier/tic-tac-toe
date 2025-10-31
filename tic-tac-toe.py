import random
import time

# Affichage du plateau de jeu
def afficher_grille(plateau):
    """Affiche l'état actuel du plateau avec index de chaque case"""
    for i in range(0, 9, 3):
        print(f" {plateau[i]} | {plateau[i+1]} | {plateau[i+2]}")
        if i < 6:
            print("---+---+---")
    print()


# Vérifie qui gagne
def verifier_gagnant(plateau):
    """Retourne 'X' ou 'O' si un joueur a gagné ou 'N' pour nul"""
    combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # lignes
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colonnes
        (0, 4, 8), (2, 4, 6)              # diagonales
    ]
    for a, b, c in combos:
        if plateau[a] != ' ' and plateau[a] == plateau[b] == plateau[c]:
            return plateau[a]
    if all(cell != ' ' for cell in plateau):
        return 'N'
    return None


def coups_disponibles(plateau):
    """Retourne la liste des cases vides"""
    return [i for i, cell in enumerate(plateau) if cell == ' ']


# Jeu de l'IA niveau débutant
def coup_ia_nv_debutant(plateau):
    """L'IA choisit un coup aléatoire parmi les cases disponibles"""
    coups = coups_disponibles(plateau)
    if coups:
        return random.choice(coups)
    return None


# Algorithme Minimax pour l'IA expert
def minimax(plateau, profondeur, est_maximisant, joueur_ia, joueur_humain):
    """
    Implémentation de l'algorithme Minimax.
    Retourne le meilleur score possible pour l'état actuel du plateau avec :
        plateau: État actuel du jeu
        profondeur: Niveau de profondeur dans l'arbre de recherche
    """
    # verifier l'etat du plateau
    gagnant = verifier_gagnant(plateau)
    
    # Si l'IA a gagné, retourner un score positif
    if gagnant == joueur_ia:
        return 10 - profondeur  # Favorise les victoires rapides
    
    # Si l'humain a gagné, retourner un score négatif
    if gagnant == joueur_humain:
        return profondeur - 10  # Favorise les défaites tardives
    
    # Si match nul
    if gagnant == 'N':
        return 0
    
    # Tour de l'IA (maximisant) - cherche le score maximum
    if est_maximisant:
        meilleur_score = float('-inf')
        
        for coup in coups_disponibles(plateau):
            # Simuler le coup
            plateau[coup] = joueur_ia
            
            # Appel pour le tour suivant (minimisant)
            score = minimax(plateau, profondeur + 1, False, joueur_ia, joueur_humain)
            
            # Annuler le coup
            plateau[coup] = ' '
            
            # Garder le meilleur score
            meilleur_score = max(score, meilleur_score)
        
        return meilleur_score
    
    # Tour de l'humain (minimisant) - cherche le score minimum
    else:
        meilleur_score = float('inf')
        
        for coup in coups_disponibles(plateau):
            # Simuler le coup
            plateau[coup] = joueur_humain
            
            # Appel récursif pour le tour suivant (maximisant)
            score = minimax(plateau, profondeur + 1, True, joueur_ia, joueur_humain)
            
            # Annuler le coup
            plateau[coup] = ' '
            
            # Garder le meilleur score (minimum)
            meilleur_score = min(score, meilleur_score)
        
        return meilleur_score


def coup_ia_nv_expert(plateau, joueur_ia='O', joueur_humain='X'):
    """
    Trouve le meilleur coup pour l'IA en utilisant l'algorithme Minimax.
    et donne l'index du meilleur coup à jouer
    """
    meilleur_score = float('-inf')
    meilleur_coup = None
    
    # Évaluer chaque coup disponible
    for coup in coups_disponibles(plateau):
        # Simuler le coup
        plateau[coup] = joueur_ia
        
        # Calculer le score avec Minimax (l'humain joue ensuite)
        score = minimax(plateau, 0, False, joueur_ia, joueur_humain)
        
        # Annuler le coup
        plateau[coup] = ' '
        
        # Garder le meilleur coup
        if score > meilleur_score:
            meilleur_score = score
            meilleur_coup = coup
    
    return meilleur_coup


def choisir_mode():
    """Permet au joueur de choisir le mode de jeu: pvp, ia débutant ou expert"""
    while True:
        print("\nChoisissez le mode de jeu :")
        print("1 - Joueur contre Joueur")
        print("2 - Joueur contre IA Débutant")
        print("3 - Joueur contre IA Expert")
        choix = input("Votre choix (1, 2 ou 3) : ")
        
        if choix == '1':
            return 'pvp'
        elif choix == '2':
            return 'ia_debutant'
        elif choix == '3':
            return 'ia_expert'
        else:
            print("Entrée invalide. Tapez 1, 2 ou 3.")


def boucle_de_jeu():
    """Boucle principale du jeu"""
    plateau = [' '] * 9
    joueur = 'X'
    mode = choisir_mode()
    
    print("\n=== DÉBUT DE LA PARTIE ===\n")

    while True:
        afficher_grille(plateau)
        gagnant = verifier_gagnant(plateau)
        
        # Vérifier si la partie est terminée
        if gagnant == 'X' or gagnant == 'O':
            print(f" Le joueur {gagnant} a gagné !")
            break
        if gagnant == 'N':
            print("  Match nul.")
            break

        # Tour du joueur humain
        if mode == 'pvp' or (mode in ['ia_debutant', 'ia_expert'] and joueur == 'X'):
            try:
                coup = input(f"Joueur {joueur} — entrez une case (1-9) : ")
                if coup.lower() in ('q', 'quit', 'exit'):
                    print("Abandon du jeu.")
                    break
                
                pos = int(coup) - 1  # car l'indexation commence à 0
                
                if pos < 0 or pos > 8:
                    print("  Veuillez entrer un nombre entre 1 et 9.")
                    continue
                
                if plateau[pos] != ' ':
                    print(" Case déjà occupée, choisissez-en une autre.")
                    continue
                
                plateau[pos] = joueur
                
            except ValueError:
                print(" Entrée invalide — tapez un chiffre de 1 à 9, ou 'q' pour quitter.")
                continue

        # Tour de l'IA
        elif joueur == 'O':
            print(" L'IA réfléchit...")
            print("bip")
            time.sleep(1)
            print("bip")
            time.sleep(1)
            print("bip")
            time.sleep(1)
            
            if mode == 'ia_debutant':
                pos = coup_ia_nv_debutant(plateau)
            elif mode == 'ia_expert':
                pos = coup_ia_nv_expert(plateau, joueur_ia='O', joueur_humain='X')
            
            if pos is not None:
                plateau[pos] = joueur
                print(f"Go ! L'IA joue la case {pos + 1}\n")

        # Changement de joueur
        joueur = 'O' if joueur == 'X' else 'X'


if __name__ == "__main__":
    print("         TIC-TAC-TOE")
    print("\nNumérotation des cases :")
    print(" 1 | 2 | 3")
    print("---+---+---")
    print(" 4 | 5 | 6")
    print("---+---+---")
    print(" 7 | 8 | 9")
    print()
    
    boucle_de_jeu()
    
    
    print("Merci d'avoir joué !")
