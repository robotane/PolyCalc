# PolyCalc

Calculatrice de polynômes en Python : parsing d'expressions polynomiales via une
grammaire BNF (module `pyparsing`), et arithmétique sur ces polynômes (addition,
multiplication, réduction modulaire).

## Contenu

- `polyparse.py` — grammaire et parsing des expressions polynomiales
- `polynomials.py` / `polynomial_mod.py` — représentation et opérations sur les polynômes
- `modulo.py` — arithmétique modulaire
- `PolynomialBNF.py` — définition de la grammaire BNF
- `test_polynomials.py` — tests

## Usage

```bash
python main.py
```

Projet réalisé dans un cadre d'apprentissage du parsing et de la manipulation
symbolique en Python.
