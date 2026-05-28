from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

try:
    from parser import ReceiptData
except ImportError:
    from .parser import ReceiptData


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "receipts.db"


@dataclass
class ReceiptRecord:
    id: int
    filename: str
    merchant: str | None
    receipt_date: str | None
    subtotal: float | None
    tax: float | None
    total: float | None
    raw_text: str
    created_at: str


def get_connection(
    database_path: str | Path = DB_PATH,
) -> sqlite3.Connection:
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(
    database_path: str | Path = DB_PATH,
) -> None:
    with get_connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                merchant TEXT,
                receipt_date TEXT,
                subtotal REAL,
                tax REAL,
                total REAL,
                raw_text TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_receipt(
    filename: str,
    receipt: ReceiptData,
    database_path: str | Path = DB_PATH,
) -> int:
    initialize_database(database_path)

    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO receipts (
                filename,
                merchant,
                receipt_date,
                subtotal,
                tax,
                total,
                raw_text
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                filename,
                receipt.merchant,
                receipt.receipt_date,
                receipt.subtotal,
                receipt.tax,
                receipt.total,
                receipt.raw_text,
            ),
        )
        return int(cursor.lastrowid)


def get_receipt(
    receipt_id: int,
    database_path: str | Path = DB_PATH,
) -> ReceiptRecord | None:
    initialize_database(database_path)

    with get_connection(database_path) as connection:
        row = connection.execute(
            """
            SELECT
                id,
                filename,
                merchant,
                receipt_date,
                subtotal,
                tax,
                total,
                raw_text,
                created_at
            FROM receipts
            WHERE id = ?
            """,
            (receipt_id,),
        ).fetchone()

    if row is None:
        return None

    return ReceiptRecord(
        id=row["id"],
        filename=row["filename"],
        merchant=row["merchant"],
        receipt_date=row["receipt_date"],
        subtotal=row["subtotal"],
        tax=row["tax"],
        total=row["total"],
        raw_text=row["raw_text"],
        created_at=row["created_at"],
    )


def list_receipts(
    limit: int = 20,
    database_path: str | Path = DB_PATH,
) -> list[ReceiptRecord]:
    initialize_database(database_path)

    with get_connection(database_path) as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                filename,
                merchant,
                receipt_date,
                subtotal,
                tax,
                total,
                raw_text,
                created_at
            FROM receipts
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        ReceiptRecord(
            id=row["id"],
            filename=row["filename"],
            merchant=row["merchant"],
            receipt_date=row["receipt_date"],
            subtotal=row["subtotal"],
            tax=row["tax"],
            total=row["total"],
            raw_text=row["raw_text"],
            created_at=row["created_at"],
        )
        for row in rows
    ]


__all__ = [
    "DB_PATH",
    "ReceiptRecord",
    "get_connection",
    "get_receipt",
    "initialize_database",
    "list_receipts",
    "save_receipt",
]
