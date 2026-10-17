from collections.abc import Callable

CATEGORIES = ("billing", "shipping", "account_access", "refund", "product_defect")
FIELD_NAMES = ("order_id", "customer_name", "product_sku")

Agent = Callable[[str], str]
