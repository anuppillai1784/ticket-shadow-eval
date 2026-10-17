import random

from shadow_eval.model import CATEGORIES, FIELD_NAMES
from shadow_eval.templates import (
    BODY_TEMPLATES,
    DECOY_LINES,
    ESCALATION_LINES,
    FIELD_PHRASES,
    FIRST_NAMES,
    LAST_NAMES,
)

TICKET_COUNT = 100
MISSING_FIELD_RATE = 0.2
MULTI_ISSUE_RATE = 0.3
ESCALATION_RATE = 0.2
DECOY_RATE = 0.15
TYPO_RATE = 0.35
MIN_TYPO_WORD_LENGTH = 4
PUNCTUATION = ".,"


def generate_tickets(seed, count=TICKET_COUNT):
    rng = random.Random(seed)
    return [_make_ticket(index, rng) for index in range(count)]


def swap_adjacent_letters(word, rng):
    position = rng.randrange(len(word) - 1)
    letters = list(word)
    letters[position], letters[position + 1] = letters[position + 1], letters[position]
    return "".join(letters)


def _make_ticket(index, rng):
    category = CATEGORIES[index % len(CATEGORIES)]
    fields = {name: _field_value(name, rng) for name in FIELD_NAMES}
    escalate = rng.random() < ESCALATION_RATE
    sentences = _body_sentences(category, rng) + _field_sentences(fields, rng)
    if escalate:
        sentences.append(rng.choice(ESCALATION_LINES))
    elif rng.random() < DECOY_RATE:
        sentences.append(rng.choice(DECOY_LINES))
    text = " ".join(sentences)
    if rng.random() < TYPO_RATE:
        text = _add_typo(text, rng)
    return {
        "id": f"T-{index + 1:03d}",
        "text": text,
        "truth": {"category": category, "fields": fields, "escalate": escalate},
    }


def _body_sentences(category, rng):
    sentences = [rng.choice(BODY_TEMPLATES[category])]
    if rng.random() < MULTI_ISSUE_RATE:
        other = rng.choice([name for name in CATEGORIES if name != category])
        sentences.append(rng.choice(BODY_TEMPLATES[other]))
    return sentences


def _field_value(name, rng):
    if rng.random() < MISSING_FIELD_RATE:
        return None
    if name == "order_id":
        return f"ORD-{rng.randint(10000, 99999)}"
    if name == "customer_name":
        return f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
    return f"QP-{rng.randint(100, 999)}"


def _field_sentences(fields, rng):
    sentences = []
    for name in FIELD_NAMES:
        value = fields[name]
        if value is None:
            sentences.append(rng.choice(FIELD_PHRASES[name]["missing"]))
        else:
            sentences.append(rng.choice(FIELD_PHRASES[name]["present"]).format(value=value))
    return sentences


def _add_typo(text, rng):
    words = text.split(" ")
    candidates = [index for index, word in enumerate(words) if _is_typo_candidate(word)]
    index = rng.choice(candidates)
    core = words[index].rstrip(PUNCTUATION)
    words[index] = swap_adjacent_letters(core, rng) + words[index][len(core):]
    return " ".join(words)


def _is_typo_candidate(word):
    core = word.rstrip(PUNCTUATION)
    return len(core) >= MIN_TYPO_WORD_LENGTH and core.isalpha() and core.islower()
