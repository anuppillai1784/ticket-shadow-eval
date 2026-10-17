BODY_TEMPLATES = {
    "billing": (
        "I was charged twice for my plan this month.",
        "The invoice shows a payment I did not make.",
        "My card statement has an extra fee on it.",
    ),
    "shipping": (
        "My parcel has not arrived and the tracking has stopped.",
        "The delivery date passed a week ago with no package.",
        "The courier marked my box as delivered, but I have nothing.",
    ),
    "account_access": (
        "I cannot log in since the password reset email never came.",
        "My account is locked after several failed sign-in attempts.",
        "The two-factor code is not accepted on my phone.",
    ),
    "refund": (
        "I returned the item last week and still have no refund.",
        "Please refund my order, the return was accepted by mail.",
        "The refund was promised but the money has not come back.",
    ),
    "product_defect": (
        "The device stopped working after two days of normal use.",
        "The screen has a crack that was not there when I opened the box.",
        "The battery drains in under an hour on a full charge.",
    ),
}

FIELD_PHRASES = {
    "order_id": {
        "present": ("My order number is {value}.", "This is about order {value}."),
        "missing": ("I cannot find my order number.", "I no longer have the order number."),
    },
    "customer_name": {
        "present": ("My name is {value}.", "This is {value} writing to you."),
        "missing": ("I would rather not give my name here.", "Please check the details on file."),
    },
    "product_sku": {
        "present": ("The item is {value}.", "It is model {value}."),
        "missing": ("I do not know the model number.", "The model label is worn off."),
    },
}

ESCALATION_LINES = (
    "I am going to contact my lawyer about this.",
    "The unit overheated and burned my hand.",
    "My attorney will be in touch about this.",
)

DECOY_LINES = (
    "The courier left the box by the fire escape.",
    "The carton was not burned, only dented.",
)

FIRST_NAMES = ("Mara", "Tobin", "Ilse", "Corvin", "Bex", "Janik", "Odile", "Pell")
LAST_NAMES = ("Quorrin", "Delmont", "Ashgrove", "Pindle", "Tessaly", "Varnick", "Brenning", "Korvane")
