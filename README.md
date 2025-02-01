
# **TP Évaluation de Concurrence**

Ce projet a pour objectif d'explorer et de comparer plusieurs approches pour l'exécution parallèle de calculs intensifs. La tâche centrale consiste à résoudre des systèmes linéaires en inversant des matrices de grande dimension.

---

## **Description**

L'architecture du système se compose des modules suivants :

- **Gestionnaire de Queue (QueueManager.py)**
  Responsable de la centralisation des files de tâches et de résultats, ce module permet aux différents processus de communiquer efficacement.

- **Responsable (Boss)**
  Ce composant génère les tâches de calcul, les envoie dans la file de tâches et récupère les résultats une fois les traitements effectués.

- **Ouvriers (Minions)**
  Ces processus effectuent les calculs demandés (inversion de matrices) et renvoient les résultats dans la file de résultats.

### **Types d’Ouvriers**
1. **Ouvrier Python (Minion.py)**
   Implémenté en Python, il exploite les capacités d'optimisation de **NumPy** pour accélérer les opérations de calcul.

2. **Ouvrier C++ (low_level.cpp)**
   Développé en C++, cet ouvrier communique avec le gestionnaire de file à travers un proxy Python (proxy.py) afin d'échanger des données sérialisées.

---

## **Installation et Compilation**

### **Clonage du Repository**
Assurez-vous d’avoir installé l’outil **uv**. Ensuite, synchronisez les dépendances en exécutant :
```bash
uv sync --dev
```

### **Compilation de l’Ouvrier C++**
Pour compiler le module C++ :
```bash
# Configuration du projet
cmake -B build -S .

# Compilation
cmake --build build
```

---

## **Tests et Résultats**

### **1. Comparaison entre l’Ouvrier Python et l’Ouvrier C++**
Des tests ont été réalisés sur des matrices de dimension fixe (500×500). Les temps mesurés concernent uniquement l'inversion de la matrice.

#### **Cas 1 : 1 Ouvrier Python**
- Nombre de tâches : 20
- Nombre d’ouvriers : 1
- Temps total (s) : **0.0720**

#### **Cas 2 : 1 Ouvrier C++**
- Nombre de tâches : 20
- Nombre d’ouvriers : 1
- Temps total (s) : **0.2100**

**Observation :**
L’implémentation Python tire profit des optimisations de NumPy et s’avère environ 2,9 fois plus rapide que la version C++ dans ce scénario spécifique.

---

### **2. Impact de la Concurrence sur la Performance**
Les expérimentations suivantes illustrent l’effet de la parallélisation sur le temps global d’exécution.
- Taille des matrices : 1500×1500
- Nombre de tâches : 100
- Les ouvriers sont lancés dans des processus distincts via le script `execute_minions.sh`.

#### **Scénario A : 1 Ouvrier Python**
- Nombre d’ouvriers : 1
- Temps global (s) : **22.00**

#### **Scénario B : 2 Ouvriers Python**
- Nombre d’ouvriers : 2
- Temps global (s) : **13.50**

#### **Scénario C : 4 Ouvriers Python**
- Nombre d’ouvriers : 4
- Temps global (s) : **12.00**

#### **Scénario D : 6 Ouvriers Python**
- Nombre d’ouvriers : 6
- Temps global (s) : **12.80**

#### **Scénario E : 12 Ouvriers Python**
- Nombre d’ouvriers : 12
- Temps global (s) : **13.50**

---

### **Conclusion**
Les résultats obtenus démontrent que la parallélisation permet de réduire significativement le temps d’exécution :
- En mode mono-processus, le temps total atteint environ **22 secondes**.
- Le déploiement de plusieurs ouvriers diminue le temps global, atteignant un minimum d’environ **12 secondes** avec 4 ouvriers.
- Au-delà de 4 ouvriers, les gains se stabilisent et la surcharge de gestion des processus commence à réduire l’efficacité.

Ces observations sont en lien direct avec la configuration matérielle utilisée (notamment, un processeur à 12 cœurs physiques) ainsi qu’avec les processus concurrents en arrière-plan.

---

## **Ordre d’Exécution Recommandé**
1. **Lancement du Gestionnaire de File (QueueManager)**
2. **Exécution du Responsable (Boss)**
3. **Démarrage des Ouvriers (Minions) Python ou du Proxy associé à l’Ouvrier C++**

---
