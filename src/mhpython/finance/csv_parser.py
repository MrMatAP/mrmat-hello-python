#  MIT License
#
#  Copyright (c) 2025 Mathieu Imfeld
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import typing
import pathlib
import argparse
import datetime
import csv
from typing import Generator

from sqlalchemy import String, Date, DateTime, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column, Session

from mhpython import __version__
from mhpython.finance.db import db, ORMBase


class CSVTransaction(ORMBase):
    __tablename__ = 'csv_transactions'
    txid: Mapped[str] = mapped_column(String(16), primary_key=True)
    settlement: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    booking: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    valuta: Mapped[datetime.date] = mapped_column(Date)
    currency: Mapped[str] = mapped_column(String(3))
    debit: Mapped[float] = mapped_column(Float, default=0.0)
    credit: Mapped[float] = mapped_column(Float, default=0.0)
    saldo: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(4000))
    notes: Mapped[str] = mapped_column(String(4000), nullable=True)

    @staticmethod
    def parse_float(value: str) -> float:
        try:
            return float(value)
        except ValueError:
            return 0.0

    @staticmethod
    def from_csv(tx: typing.Dict) -> 'CSVTransaction':
        t = CSVTransaction(
            txid=tx['Transaktions-Nr.'],
            valuta=datetime.datetime.strptime(tx['Valutadatum'], '%Y-%m-%d'),
            currency=tx['Währung'],
            debit=CSVTransaction.parse_float(tx['Belastung']),
            credit=CSVTransaction.parse_float(tx['Gutschrift']),
            saldo=float(tx['Saldo']),
            description=f'{tx["Beschreibung1"]}\n{tx["Beschreibung2"]}\n{tx["Beschreibung3"]}',
            notes=tx['Fussnoten'],
        )
        try:
            t.booking = datetime.datetime.strptime(tx['Buchungsdatum'], '%Y-%m-%d')
        except ValueError:
            print(f'WARNING: Transaction {t.txid} has no booking date')
        try:
            t.settlement = datetime.datetime.strptime(
                f'{tx["\ufeffAbschlussdatum"]} {tx["Abschlusszeit"]}',
                '%Y-%m-%d %H:%M:%S',
            )
        except ValueError:
            print(f'WARNING: Transaction {t.txid} has no settlement date')
        return t


def read_csv(path: pathlib.Path) -> Generator[CSVTransaction]:
    csv_dialect = csv.Sniffer().sniff(path.read_text(encoding='utf-8'))
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, dialect=csv_dialect)
        for row in reader:
            yield CSVTransaction.from_csv(row)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=f'mrmat-finance-csv-parser - {__version__}'
    )
    parser.add_argument(
        '--path',
        type=pathlib.Path,
        required=True,
        dest='path',
        help='Path to the folder containing a CSV export',
    )
    parser.add_argument(
        '--db-url',
        type=str,
        required=True,
        dest='db_url',
        help='The database URL, in the format postgresql+psycopg2://USER:PASS@HOST/DB',
    )
    args = parser.parse_args()
    engine = db(args.db_url)
    try:
        with Session(engine) as session:
            for tx in read_csv(args.path):
                session.add(tx)
            session.commit()
        return 0
    except SQLAlchemyError as se:
        print(f'Database error: Failed to update database: {se}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
