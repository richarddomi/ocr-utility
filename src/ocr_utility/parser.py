from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ReceiptData:
    merchant: str | None
    receipt_date: str | None
    subtotal: float | None
    tax: float | None
    total: float | None
    raw_text: str


def find_money_value(pattern: str, text: str) -> float | None:
    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        return None

    value = match.group(1).replace(",", "")

    try:
        return float(value)
    except ValueError:
        return None


def parse_receipt_text(text: str) -> ReceiptData:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    merchant = lines[0] if lines else None

    date_match = re.search(
        r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",
        text,
    )

    receipt_date = date_match.group(1) if date_match else None

    subtotal = find_money_value(
        r"\bsubtotal\b\s*[:\-]?\s*\$?(\d+\.\d{2})",
        text,
    )

    tax = find_money_value(
        r"\btax\b\s*[:\-]?\s*\$?(\d+\.\d{2})",
        text,
    )

    total = find_money_value(
        r"\btotal\b\s*[:\-]?\s*\$?(\d+\.\d{2})",
        text,
    )

    return ReceiptData(
        merchant=merchant,
        receipt_date=receipt_date,
        subtotal=subtotal,
        tax=tax,
        total=total,
        raw_text=text,
    )


__all__ = [
    "ReceiptData",
    "find_money_value",
    "parse_receipt_text",
]
