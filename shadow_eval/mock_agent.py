import json
import re
import zlib

from shadow_eval.model import CATEGORIES

UNKNOWN_CATEGORY = "unknown"
PERCENT_BUCKETS = 100

CATEGORY_KEYWORDS = (
    ("account_access", ("log in", "password", "locked", "two-factor", "sign-in")),
    ("shipping", ("parcel", "delivery", "courier", "tracking", "box")),
    ("billing", ("charged", "invoice", "fee", "payment")),
    ("refund", ("refund", "return")),
    ("product_defect", ("stopped working", "crack", "battery", "device")),
)
ESCALATION_KEYWORDS = ("lawyer", "burn", "injur", "police")
FLIP_PERCENT = {
    "billing": 10,
    "shipping": 10,
    "account_access": 5,
    "refund": 20,
    "product_defect": 25,
}
ORDER_ID_PATTERN = re.compile(r"(ORD-\d{5})")
SKU_PATTERN = re.compile(r"(QP-\d{3})")
NAME_PATTERN = re.compile(r"My name is ([A-Z][a-z]+ [A-Z][a-z]+)")


def mock_agent(text):
    """Return a deterministic, imperfect JSON prediction for one ticket text."""
    prediction = {
        "category": _classify(text),
        "fields": {
            "order_id": _search(ORDER_ID_PATTERN, text),
            "customer_name": _search(NAME_PATTERN, text),
            "product_sku": _search(SKU_PATTERN, text),
        },
        "escalate": _mentions_escalation(text),
    }
    return json.dumps(prediction, sort_keys=True)


def _classify(text):
    lowered = text.lower()
    category = next(
        (
            name
            for name, keywords in CATEGORY_KEYWORDS
            if any(keyword in lowered for keyword in keywords)
        ),
        UNKNOWN_CATEGORY,
    )
    if category != UNKNOWN_CATEGORY and _is_flipped(text, category):
        return _next_category(category)
    return category


def _is_flipped(text, category):
    bucket = zlib.crc32(text.encode("utf-8")) % PERCENT_BUCKETS
    return bucket < FLIP_PERCENT[category]


def _next_category(category):
    return CATEGORIES[(CATEGORIES.index(category) + 1) % len(CATEGORIES)]


def _mentions_escalation(text):
    lowered = text.lower()
    return any(keyword in lowered for keyword in ESCALATION_KEYWORDS)


def _search(pattern, text):
    match = pattern.search(text)
    return match.group(1) if match else None
