# CV-Normalization
## Introduction

Cet outil a été conçu pour aider les professionnels des ressources humaines (RH) dans le processus de normalisation des CV des candidats avant de les envoyer aux clients, en éliminant les identifiants personnels. Il prend un CV au format PDF et génère, en retour, un CV adapté à un modèle choisi par les RH, que l'utilisateur peut télécharger au format HTML, PDF ou DOC. Ce processus permet de gagner un temps considérable en automatisant la normalisation des CV, tout en garantissant que les informations sensibles ne soient pas partagées avec les clients.

## Différentes approches testées

Dans un premier temps, j'ai essayé de reproduire la méthode utilisée pour l'analyse des CV afin de générer des fichiers JSON pour alimenter la base de données, en utilisant Mistral OCR et Mistral Small. L'OCR extrayait le texte du PDF et le transmettait ensuite à Mistral Small, qui était invité à organiser les informations conformément au modèle. Cette approche a donné de bons résultats, mais elle n'a pas toujours réussi à identifier correctement les noms et, parfois, oubliait certains détails du prompt. De plus, avec cette version, il n'était possible de télécharger le résultat qu'en PDF ou HTML.

Dans une deuxième tentative, j'ai intégré Streamlit avec Quill pour permettre la modification directe du résultat. L'idée était d'améliorer la qualité du résultat généré, mais après l'ajout de cette fonctionnalité, le modèle a cessé de prendre en compte le prompt, et le résultat final était de mauvaise qualité, au point qu'il n'était même pas possible de le corriger via l'outil de modification ajouté.

Pour la version suivante, j'ai permis le téléchargement des résultats au format Word, afin de faciliter les modifications et de pouvoir les enregistrer à nouveau.

Dans la version suivante, pour résoudre le problème rencontré avec l'LLM, j'ai testé OpenAI GPT-4o, qui offrait de bonnes performances. Cependant, j'ai constaté qu'il ne pouvait pas traiter un fichier directement ni effectuer l'OCR. Nous avons alors travaillé avec PyMuPDF, qui a extrait le texte de manière très efficace. Cela m'a conduit à utiliser PyMuPDF pour l'extraction du texte et à conserver Mistral Small pour organiser les données selon le modèle. C'est cette version que nous présentons aujourd'hui.

Concernant le modèle/template, une réunion a eu lieu avec l'équipe RH pour apporter quelques ajustements, comme placer le logo en haut à droite plutôt qu'à gauche, et transformer les différentes sections du CV en boîtes pour une meilleure lisibilité.

Cette approche permet désormais une extraction de texte fiable et une organisation cohérente des informations, tout en offrant des options de téléchargement variées.

## Tutoriel : Comment exécuter l'application

### **Étape 1 : Télécharger et extraire le dossier**

1. Téléchargez le dossier contenant les fichiers suivants :
    - `requirements.txt`
    - `app.py`

### **Étape 2 : Installer Python (si ce n'est pas déjà fait)**

1. Si Python n'est pas déjà installé sur votre machine, téléchargez et installez la dernière version de [Python](https://www.python.org/downloads/).
2. Pendant l'installation, veillez à cocher la case **"Ajouter Python au PATH"**.

### **Étape 3 : Configurer un environnement virtuel**

1. Accédez au dossier du projet :
    - Ouvrez un terminal (ou une invite de commande) et accédez au dossier où vous avez sauvegardé les fichiers du projet avec la commande suivante :
        
        ```bash
        bash
        cd chemin/vers/votre/dossier
        ```
        
2. Créez un environnement virtuel :
    - Exécutez la commande suivante pour créer un environnement virtuel (nommez-le `env` ou un autre nom de votre choix) :
        
        ```bash
        bash
        python -m venv env
        ```
        

### **Étape 4 : Activer l'environnement virtuel**

1. Activez l'environnement virtuel :
    - Sous Windows :
        
        ```bash
        bash
        .\env\Scripts\activate
        ```
        
    - Sous Mac/Linux :
        
        ```bash
        bash
        source env/bin/activate
        ```
        
2. Après activation, votre terminal affichera le nom de l'environnement virtuel (par exemple, `(env)`).

### **Étape 5 : Installer les dépendances**

1. Installez les packages Python requis :
    - Assurez-vous que l'environnement virtuel est activé.
    - Exécutez la commande suivante pour installer toutes les dépendances listées dans le fichier `requirements.txt` :
        
        ```bash
        bash
        pip install -r requirements.txt
        ```
        

### **Étape 6 : Exécuter l'application Streamlit**

1. Exécutez l'application Streamlit :
    - Une fois les dépendances installées, lancez l'application avec la commande suivante :
        
        ```bash
        bash
        streamlit run app.py
        ```
        
2. Cela démarrera le serveur Streamlit, et l'application s'ouvrira automatiquement dans votre navigateur. Si ce n'est pas le cas, vous pouvez naviguer manuellement vers [http://localhost:8501](http://localhost:8501/) pour accéder à l'application.

### **Étape 7 : Désactiver l'environnement virtuel (optionnel)**

1. Une fois que vous avez fini d'utiliser l'application, vous pouvez désactiver l'environnement virtuel avec la commande suivante :
    
    ```bash
    bash
    deactivate
    ```
    
    Cela vous ramènera à l'environnement Python global.
