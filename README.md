# Mise en place de modèle de scoring pour le scoring d'une base de donnée de clients

Ce projet centralise les travaux fait sur la mise en place de modèle de scoring d'une base de données de clients réalisés au cours de ma formatioin Ingénieur IA chez OpenClassroom

## Présentation des données

Les objectifs du projet était de fournir un outil permettant d'identifier la capacité de remboursement d'une crédit par le client. La probabilité de défaut est calculée. Le coût d'une erreur de décision est pris en compte. Des outils d'interprétion de l'importance des variables amenant à la décision sont également mis en place.


Les données sont issues de cette [compétition kaggle](https://www.kaggle.com/competitions/home-credit-default-risk). Elles se présentent en plusieurs fichiers organisés comme 

![Organisation des données](https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/organisation_donnees.png)

Dans ce repo, vous trouverez :
- L'analyse univariée des données dans les notebooks uniAnalysis_[*].ipynb (séparés par fichier pour la clarté)
- La concaténation de ces fichiers
- L'EDA des fichiers combinés dans le notebook EDA.ipynb,
- La mise en place et la comparaison des modèles de scoring,
- Le feature engineering pour comprendre les modèles.

### Mise en place des modèles, GridSearch avec pipeline, Fonction de coûts
La mise en place des modèles et l'optimisation des hyper-paramètres se font avec l'utilisation de pipelines qui comprennent les étapes suivantes :
- Fold stratification,
- Scaling,
- Oversampling, undersampling,
- Entrainement du modèle.

![Pipeline](https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/pipeline.png)

L'évaluation du modèle se fait à l'aide du $F_\beta$-score ($\beta = 2$). Une fonction métier prenant en compte la perte d'argent entrainée par une erreur peut aussi être mise en place :
- Perte dues à un faux positif : Intérêt du prêt et perte du client
- Perte dues à un faux négatif : Montant du prêt non recouvré et frais des procédures légales

Différents algorithmes sont testés :
- Linear SVC
- kNN classifier
- Random forest
- Gradient boosting

La synthèse des performances est résumée ci-desssous

![tableau-perf](https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/tableau-perf.png) ![graph-perf](https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/graph-perf.png)

### Impact des variables

Deux méthodes de feature importance sont testées :
- Permutation Feature Importance - méthode globale
- LIME - méthode locale

![PFI](https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/PFI.png) ![LIME](https://raw.githubusercontent.com/QuDbo/project-scoring-ML/main/img/LIME.png)