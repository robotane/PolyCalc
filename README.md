# PolyCalc

Calculatrice de polynômes en Python, avec deux interfaces expérimentales
distinctes autour d'une même représentation interne des polynômes.

## Le modèle de polynômes (`polynomials/`)

Le cœur du projet : des classes représentant un polynôme comme une liste de
monômes (coefficient + degré), avec les opérations arithmétiques usuelles
(addition, multiplication, etc.) :

- `Monomial.py` — un monôme (coefficient en `Fraction`, degré)
- `Polynomial.py` — un polynôme, liste de monômes
- `ModuloPolynomial.py` — variante où les coefficients sont réduits modulo `n`
- `RationalPolynomial.py` — variante à coefficients rationnels

`modulo.py` fournit l'arithmétique modulaire (classe `NZ`) utilisée par
`ModuloPolynomial`.

## Interface 1 : calculatrice graphique (`main.py`)

Une interface PyQt5 façon calculatrice (pavé numérique + opérateurs
polynomiaux `x`, `^`) permettant d'insérer des polynômes et d'enchaîner des
calculs dessus (`P1 + P2`, etc.), avec un historique affiché.

```bash
python main.py
```

## Interface 2 : parseur en ligne de commande (`polyparse.py`)

Un parseur d'expressions polynomiales bâti sur une grammaire BNF
(`PolynomialBNF.py`, via `pyparsing`), utilisable en REPL pour taper
directement des expressions et des affectations (`f = x + 5 - 7x^3`) :

```bash
python polyparse.py
```

Les deux interfaces sont des expérimentations indépendantes autour du même
modèle de polynômes — `polyparse.py` ne remplace pas encore `main.py`, comme
en témoigne le TODO laissé dans `main.py` à ce sujet.

Projet réalisé dans un cadre d'apprentissage du parsing et de la manipulation
symbolique en Python.
