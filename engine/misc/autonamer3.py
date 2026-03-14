from engine.libs.mersenne_twister import choice, random
from engine.globs.mod_data import ModData
from datetime import datetime
import re, unicodedata
from os import path
import hashlib


def hashed_seed(base_seed: str | float | int = None):
    """
    Genera una seed a partir del tiempo actual si no se pasa una explícita.
    """
    if base_seed is None:
        base_seed = ''.join(c for c in str(datetime.now()) if c.isdigit())  # esto mismo hace ModData.genearte_id()
    elif type(base_seed) in (int, float):
        base_seed = str(base_seed)
    else:
        raise TypeError(f"if provided, type(base_seed) must be str, float or int, not {type(base_seed)}")
    return int(hashlib.sha256(base_seed.encode("utf-8")).hexdigest(), 16) & 0xFFFFFFFF


def load_rul(filename, grammar=None, replacements=None, loaded=None):
    if grammar is None:
        grammar = {}
    if replacements is None:
        replacements = []
    if loaded is None:
        loaded = set()

    if filename in loaded:
        return grammar, replacements
    loaded.add(filename)

    current_rule = None

    base_dir = path.dirname(filename)

    with open(path.join(ModData.game_fd, filename), encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()

            if not line or line.startswith("//"):
                continue

            if line.startswith("#include"):
                include_file = line.split()[1]
                include_path = path.join(base_dir, include_file)
                load_rul(include_path, grammar, replacements, loaded)
                continue

            # replacements
            if "==" in line:
                a, b = line.split("==", 1)
                replacements.append((a.strip(), b.strip()))
                continue

            # detectar probabilidad
            prob = 100
            prob_match = re.search(r"\[(\d+)%]", line)
            if prob_match:
                prob = int(prob_match.group(1))
                # quitar la parte del texto de la línea, para que no quede en el resultado
                line = line[:prob_match.start()].strip()

            # regla nueva
            if "=>" in line:
                left, right = line.split("=>", 1)
                left = left.strip()
                right = right.strip()
                current_rule = left if left != '' else current_rule
                grammar.setdefault(current_rule, [])
                grammar[current_rule].append((right, prob))

            # continuación de regla
            else:
                if current_rule is None:
                    raise ValueError(f"Option without rule: {line}")

                grammar[current_rule].append((line, prob))

    return grammar, replacements


# -------------------------------
# Funciones auxiliares
# -------------------------------
def merge_parts(a, b):
    vowels = "aeiouáéíóú"
    if not a or not b:
        return a + b
    if a[-1].lower() == b[0].lower():
        return a + b[1:]
    if a[-1].lower() in vowels and b[0].lower() in vowels:
        return a + b[1:]
    return a + b


def pronounceable(name):
    vowels = "aeiouáéíóú"
    v = c = 0
    for ch in name.lower():
        if ch in vowels:
            v += 1
            c = 0
        else:
            c += 1
            v = 0
        if v >= 3 or c >= 3:
            return False
    return True


def add_spanish_accent(word):
    replacements = {"i": "í", "a": "á", "e": "é"}
    if word[-1].lower() in replacements:
        return word[:-1] + replacements[word[-1].lower()]
    return word


# -------------------------------
# Expansión de reglas RUL
# -------------------------------
# rule_pattern = re.compile(r"\{([A-Z]+)}")


def resolve_optionals(text):
    optional_pattern = re.compile(r"\[([^]]+)]")

    def replace(match):
        return match.group(1) if random() < 0.5 else ""

    return optional_pattern.sub(replace, text)


def weighted_choice(options):
    total = sum(weight for _, weight in options)
    r = random() * total
    upto = 0

    for value, weight in options:
        if upto + weight >= r:
            return value
        upto += weight

    return options[-1][0]


def expand_rule(rule, grammar, replacements=None):
    if replacements is None:
        replacements = []

    tokens = re.split(r'(\{[^}]+})', rule)
    result = []

    for token in tokens:
        if not token:
            continue

        if token.startswith("{") and token.endswith("}"):
            # Expandir símbolo
            name = token[1:-1]
            expanded = generate(name, grammar, replacements)
        else:
            expanded = token  # texto literal

        # Aplicar reemplazos
        for old, new in replacements:
            expanded = expanded.replace(old, new)

        result.append(expanded)

    return "".join(result)


def generate(symbol, grammar, replacements, gender=None):
    options = grammar[symbol]

    # Elegir opción según probabilidad
    rule = weighted_choice(options)

    # Si la regla es otra regla, expandir recursivamente
    if rule in grammar:
        return generate(rule, grammar, replacements, gender)

    # Si es literal, expandir tokens
    result = expand_rule(rule, grammar, replacements)
    result = resolve_optionals(result)
    return result


# -------------------------------
# Función principal: generator con índice y acentos
# -------------------------------
def name_generator(symbol, language: str = None, gender: str = None, just_name=False):
    grammar, replacements = load_rul("people_grammar.rul")
    index = 0
    while True:
        name: str = generate_name(symbol, grammar, replacements, language, gender=gender, just_name=just_name)
        if just_name:
            yield name
        else:
            yield index, name
        index += 1


def generate_name(symbol, grammar, replacements, language=None, gender=None, just_name=False):
    name = generate(symbol, grammar, replacements)

    parts = name.split()
    first = parts[0]

    # Si el género se pasa explícitamente, lo usamos
    if gender is None:
        gender = 'feminine' if first[-1].lower() in "aeiou" else 'masculine'

    if language is None:
        language = choice(['english', 'spanish'])

    # Aplicar acento si es español y nombre femenino
    if language == "spanish" and gender == 'feminine':
        first = add_spanish_accent(first)

    parts[0] = first
    if not just_name:
        return " ".join(parts) + f" ({gender}) #{language.capitalize()}"
    else:
        return " ".join(parts)


__all__ = [
    'name_generator'
]