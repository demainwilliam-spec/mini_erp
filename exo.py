# Backtrack combinaisons 
# # Exercice Backtracking — Permutations uniques avec doublons
 
# ## Objectif
 
# Écrire une fonction qui génère toutes les permutations possibles d'une liste.
 
# La liste peut contenir des doublons, mais le résultat ne doit contenir aucune permutation en double.
 
# ---
 
# ## Fonction à écrire
 
# ```python
def unique_permutations(items):
    res = []
    seen = set()
    
    for x in items:
        if

# ```
 
# ---
 
# ## Exemple 1
 
# Entrée :
 
# ```python
# items = ["a", "b", "c"]
# ```
 
# Sortie :
 
# ```python
# [
#     ["a", "b", "c"],
#     ["a", "c", "b"],
#     ["b", "a", "c"],
#     ["b", "c", "a"],
#     ["c", "a", "b"],
#     ["c", "b", "a"]
# ]
# ```
 
# ---
 
# ## Exemple 2
 
# Entrée :
 
# ```python
# items = ["a", "b", "a"]
# ```
 
# Sortie :
 
# ```python
# [
#     ["a", "a", "b"],
#     ["a", "b", "a"],
#     ["b", "a", "a"]
# ]
# ```
 
# Il ne doit y avoir que 3 permutations.
 
# Une mauvaise solution pourrait produire :
 
# ```python
# [
#     ["a", "a", "b"],
#     ["a", "b", "a"],
#     ["a", "a", "b"],
#     ["a", "b", "a"],
#     ["b", "a", "a"],
#     ["b", "a", "a"]
# ]
# ```
 
# Les doublons doivent être supprimés.
 
# ---
 
# ## Contraintes
# * Chaque élément doit être utilisé exactement une fois dans une permutation.
# * Ne pas retourner de permutations en double.
# * La liste peut contenir des doublons.
# * La liste peut être vide.
 
 
# ```python
# print(unique_permutations(["a", "b", "a"]))
# ```
 
# Résultat attendu :
 
# ```python
# [
#     ["a", "a", "b"],
#     ["a", "b", "a"],
#     ["b", "a", "a"]
# ]
# ```
 
# ---
 
# ```python
# print(unique_permutations([1, 2, 2]))
# ```
 
# Résultat attendu :
 
# ```python
# [
#     [1, 2, 2],
#     [2, 1, 2],
#     [2, 2, 1]
# ]
# ```
 
# ---
 
# ```python
# print(unique_permutations([]))
# ```
 
# Résultat attendu :
 
# ```python
# [
#     []
# ]
# ```
 
 