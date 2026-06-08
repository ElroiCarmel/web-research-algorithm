# Maximally-Proportional Allocation

A small Flask web app that demonstrates the **maximally-proportional allocation**
algorithm: a method for dividing a set of indivisible items among *n* agents as
fairly as possible.

I implemented this algorithm from its [original research paper](https://mpra.ub.uni-muenchen.de/56587/1/MPRA_paper_56585.pdf)
and contributed it to the open-source
[fairpyx](https://github.com/ariel-research/fairpyx) library; this app is an
interactive front-end for it.

**Live demo:** https://elroica277.csariel.xyz/

**Paper:** Brams, Kilgour & Klamler (2014), _[An algorithm for the proportional
division of indivisible items](https://mpra.ub.uni-muenchen.de/56587/1/MPRA_paper_56585.pdf)_

## What it does

Given each agent's valuations over the items, the algorithm:

1. Tries to give every agent a **proportional** bundle — one they value at least
   `1/n` of their total value over all items.
2. **Maximises the number** of agents who achieve that proportional share.
3. Among those, makes the **least-satisfied** proportional agent as happy as
   possible.

The result is a Pareto-optimal allocation meeting these three criteria. The app
lets you enter your own valuations (or generate a random example) and shows the
resulting allocation along with per-agent scores and the algorithm's log.

## Tech stack

Python · Flask · Flask-WTF · `fairpyx` · HTML/CSS (Bootstrap)

## Run locally

### With Docker (recommended)

```bash
docker build -t myapp .
docker run --rm -p 5000:5000 -e FLASK_SECRET_KEY="any-random-string" myapp
```

Then open http://localhost:5000.

### With Python

```bash
pip install -r requirements.txt
export FLASK_SECRET_KEY="any-random-string"
python app.py
```

`FLASK_SECRET_KEY` is required — Flask-WTF uses it to sign the CSRF tokens that
protect the input forms.
