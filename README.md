# Mise en place de modèle de scoring pour le scoring d'une base de donnée de clients

Ce projet centralise les travaux fait sur la mise en place de modèle de scoring d'une base de données de clients réalisés au cours de ma formatioin Ingénieur IA chez OpenClassroom

## Présentation des données

Les objectifs du projet était de fournir un outil permettant d'identifier la capacité de remboursement d'une crédit par le client. La probabilité de défaut est calculée. Le coût d'une erreur de décision est pris en compte. Des outils d'interprétion de l'importance des variables amenant à la décision sont également mis en place.


Les données sont issues de cette [compétition kaggle](https://www.kaggle.com/competitions/home-credit-default-risk). Elles se présentent en plusieurs fichiers organisés comme 

<img src="https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/organisation_donnees.png" alt="Organisation des données" width="400"/>

Dans ce repo, vous trouverez :
- L'analyse des données du fichier application dans le notebooks traitement_appTrain.ipynb
- Le traitement des fichiers annexe et la concaténation de ces fichiers au données application
- L'EDA des fichiers combinés dans le notebook EDA_etat_final.ipynb,
- La mise en place et la comparaison des modèles de scoring,
- Le feature engineering pour comprendre les modèles.

### Mise en place des modèles, GridSearch avec pipeline, Fonction de coûts
La mise en place des modèles et l'optimisation des hyper-paramètres se font avec l'utilisation de pipelines qui comprennent les étapes suivantes :
- Fold stratification,
- Scaling,
- Oversampling, undersampling,
- Entrainement du modèle.

<img alt="Pipeline" src="https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/pipeline.png" width="400"/>

L'évaluation du modèle se fait à l'aide du $F_\beta$-score ($\beta = 2$). Une fonction métier prenant en compte la perte d'argent entrainée par une erreur peut aussi être mise en place :
- Perte dues à un faux positif : Intérêt du prêt et perte du client
- Perte dues à un faux négatif : Montant du prêt non recouvré et frais des procédures légales

Différents algorithmes sont testés :
- Linear SVC
- kNN classifier
- Random forest
- Gradient boosting

La synthèse des performances est résumée ci-desssous

<img alt="tableau-perf" src="https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/tableau-perf.png" width="400"/> <img alt="graph-perf" src="https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/graph-perf.png" width="400"/>

### Impact des variables

Deux méthodes de feature importance sont testées :
- Permutation Feature Importance - méthode globale
- LIME - méthode locale

<img alt="PFI" src="https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/PFI.png" width="400"/> <img alt="LIME" src="https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/LIME.png" width="400"/>