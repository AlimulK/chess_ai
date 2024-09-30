# CHESS

An app that allows you to play chess with the standard rules.
I will be adding AI functionality at some point to allow player vs com matches.

## Instructions

* Left Mouse Click = Make move
* Z = Undo move

## Setting Up

### Setup virtual environment

Input into your terminal:

```commandline
python -m venv venv
```

This is assuming you already have Python installed (you may need to replace
`python` with `python3`).

### Activating the virtual environment

This step differs between Windows and Linux/macOS machines.

* For Windows:

```commandline
venv\Scripts\activate
```

* For Linux and macOS

```commandline
source venv/bin/activate
```

### Install the requirements

Input into your terminal:

```commandline
pip install -r requirements_user.txt
```

This will install all the libraries I have specified in `requirements_user.txt`

### Run the app

Now simply run `chess_main.py`:

```commandline
python chess_main.py
```

## Metadata

### Documentation

All the documentation is within the docs folder and was generated using `Sphinx 6.1.3`

The generated HTML is within `./docs/build/html`

### Credits

Chess Pieces by Cburnett - https://commons.wikimedia.org/w/index.php?curid=1499803
