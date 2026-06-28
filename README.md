# PDF Password Protect

A Python script that batch password-protects PDF files using AES-256 encryption.

## Requirements

- Python 3.8+
- [pikepdf](https://pikepdf.readthedocs.io/)

Install the dependency:

```bash
pip install pikepdf
```

## Usage

```bash
python protect.py /path/to/directory
```

The script processes every `.pdf` file found in the specified directory.

## Output

The script creates a sibling directory named `<input>_password_protected` next to the input directory:

```
bank_statements/
    statement_jan.pdf
    statement_feb.pdf

bank_statements_password_protected/
    statement_jan.pdf       ← encrypted copy
    statement_feb.pdf       ← encrypted copy
    _passwords.txt          ← one line per file
```

The original input directory and its files are never modified.

### _passwords.txt format

Each line records the filename and its generated password:

```
statement_jan.pdf | aB3@kZ9x
statement_feb.pdf | Qr7+mN2_w
```

The file is opened in append mode, so re-running the script against a new set of files will add entries rather than overwrite existing ones.

## Password Generation

Passwords are generated using Python's `secrets` module (cryptographically secure). Each password is:

- **Length**: 8–10 characters (chosen randomly)
- **Character set**: `a-z`, `A-Z`, `0-9`, and `@ - _ = + .`

## Encryption

Files are encrypted with AES-256 (`R=6` in PDF encryption terms) via pikepdf. Both the user password and owner password are set to the same generated value.

## Behavior

### Overwrite prompt

If the output directory already exists, the script warns you and asks before proceeding:

```
Warning: Output directory already exists: '/path/to/bank_statements_password_protected'
Output directory already exists. Overwrite? (yes/no):
```

Entering anything other than `yes` exits immediately without modifying anything.

### Processing order

Files are processed in alphabetical order by filename.

### Status output

The script prints a status line for each file and a summary at the end:

```
Processing statement_jan.pdf... done
Processing statement_feb.pdf... ERROR - <reason>

Summary: 1 succeeded, 1 failed.
Output directory : /path/to/bank_statements_password_protected
Passwords file   : /path/to/bank_statements_password_protected/_passwords.txt
```

### Error handling

| Situation | Behaviour |
|---|---|
| Input directory does not exist or is not a directory | Print error and exit |
| No PDF files found in input directory | Print message and exit |
| Output directory cannot be created | Print error and exit |
| Individual PDF fails to process | Print error for that file, continue with remaining files |
| `pikepdf` is not installed | Print install instruction and exit |
