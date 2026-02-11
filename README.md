1. Avantages observés
Quels sont les avantages de l'automatisation des tests que vous avez constatés ?

Rapidité : 7 tests exécutés en 30 secondes automatiquement vs plusieurs minutes manuellement
Fiabilité : Tous les cas sont testés systématiquement (décimaux, négatifs, division par zéro)
Détection immédiate : Si je casse quelque chose dans le code, je le sais tout de suite

Comment le CI/CD améliore-t-il la qualité du code ?

Les tests s'exécutent automatiquement à chaque push sur GitHub
Le déploiement ne se fait que si tous les tests passent
Feedback rapide : je sais en 3 minutes si mon code fonctionne


2. Défis rencontrés
Quelles difficultés avez-vous rencontrées avec Selenium ?

ChromeDriver incompatible : webdriver-manager téléchargeait le mauvais fichier sur GitHub Actions (erreur "Exec format error")

Solution : Utiliser ChromeDriver système en CI, webdriver-manager en local


Nombres décimaux refusés : Le HTML bloquait les valeurs comme "10.5"

Solution : Ajouter step="any" dans les inputs


Résultat vide dans les tests : Le test s'exécutait avant que le résultat ne s'affiche

Solution : Utiliser WebDriverWait pour attendre que le texte apparaisse



Comment pourriez-vous améliorer la stabilité des tests ?

Utiliser systématiquement WebDriverWait au lieu de sleep()
Ajouter des captures d'écran automatiques en cas d'échec
Implémenter le Page Object Pattern (déjà commencé)
Tester sur plusieurs navigateurs (Chrome, Firefox)


3. Métriques
Quelles métriques sont les plus importantes pour votre projet ?

Taux de réussite : 7/7 tests passent (100%)
Temps d'exécution : ~30 secondes en local, ~3 minutes en CI
Temps de feedback : Moins de 5 minutes après un push
Stabilité : Nombre de fois où les tests échouent à tort

Comment mesurer l'efficacité de votre pipeline CI/CD ?

Consulter l'onglet Actions sur GitHub : voir les taux de succès/échec
Temps de détection des bugs : combien de temps entre l'introduction d'un bug et sa détection (idéalement quelques minutes)
Nombre de déploiements : plus il y en a, plus l'équipe est productive
Bugs en production : un bon CI/CD = moins de bugs qui passent en prod