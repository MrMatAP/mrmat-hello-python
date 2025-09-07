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

from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import String, DateTime, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column, Session

from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFDirectoryLoader

from mhpython import __version__
from mhpython.finance.db import ORMBase, db


class Transaction(BaseModel):
    """
    A single transaction consists of the following fields. Do not extract the transaction when its 'Informationen' field contains 'Anfangssaldo' or 'Schlusssaldo'.
    Do not extract any transaction that has no 'Datum'.
    """
    date: typing.Optional[datetime.datetime] = Field(description="The 'Datum' date of the transaction")
    counterparty: typing.Optional[str] = Field(description="The 'Information' of the transaction, as a multiline string")
    debit: typing.Optional[float] = Field(description="The 'Belastungen' of the transaction, or 0 when empty", default=0)
    credit: typing.Optional[float] = Field(description="The 'Gutschriften' of the transaction, or 0 when empty", default=0)
    valuta: typing.Optional[datetime.datetime] = Field(description="The 'Valuta' date of the transaction")
    value: typing.Optional[float] = Field(description="The 'Kontostand' of the transaction", default=0)

class Statement(BaseModel):
    """
    A financial statement consists of three relevant sections:
    * A section at the top of the document on the right, containing the IBAN, Konto-Nr., Kunden-Nr., BIC and the 'Erstellt am' date
    * The 'Ihr Konto auf einen Blick' section, containing the Anfangssaldo, Gutschriften, Belastungen and Schlusssaldo
    * Multiple pages of individual transactions, each with a 'Datum', 'Belastungen', 'Gutschriften', 'Valuta' and 'Kontostand'.
      The 'Information' field is multi-line text and must be extracted as a whole, single string with the same line-breaks.
    """
    iban: str = Field(description="The value of the IBAN field on the first page")
    account_number: str = Field(description="The value of the 'Konto-Nr.' field on the first page")
    customer_number: str = Field(description="The value of the 'Kunden-Nr.' field on the first page")
    bic: str = Field(description="The value of the 'BIC' field on the first page")
    created_at: typing.Optional[datetime.datetime] = Field(description="The value of the 'Erstellt am' field on the first page")
    value_start: typing.Optional[float] = Field(description="The 'Anfangssaldo' in the 'Ihr Konto auf einen Blick' section on the first page")
    total_credit: typing.Optional[float] = Field(description="The 'Gutschriften' in the 'Ihr Konto auf einen Blick' section on the first page")
    total_debit: typing.Optional[float] = Field(description="The 'Belastungen' in the 'Ihr Konto auf einen Blick' section on the first page")
    value_end: typing.Optional[float] = Field(description="The 'Schlusssaldo' in the 'Ihr Konto auf einen Blick' section on the first page")

    transactions: typing.List[Transaction] = Field(default_factory=list, title="One entry for each transaction following the 'Ihr Konto auf einen Blick' section")

class Account(BaseModel):
    """Information about an accoun"""
    iban: str = Field(description="IBAN")
    statements: typing.List[Statement] = Field(description="Statements", default_factory=list)


class ORMTransaction(ORMBase):
    __tablename__ = 'transactions'
    id: Mapped[int] = mapped_column(primary_key=True)
    valuta: Mapped[datetime.datetime] = mapped_column(DateTime)
    counterparty: Mapped[str] = mapped_column(String(4000))
    debit: Mapped[float] = mapped_column(Float, default=0.0)
    credit: Mapped[float] = mapped_column(Float, default=0.0)
    value: Mapped[float] = mapped_column(Float)
    iban: Mapped[str] = mapped_column(String)

    @staticmethod
    def from_parsed(iban: str, tx: Transaction) -> "ORMTransaction":
        return ORMTransaction(valuta=tx.valuta,
                              counterparty=tx.counterparty,
                              debit=tx.debit,
                              credit=tx.credit,
                              value=tx.value,
                              iban=iban)

    def __repr__(self):
        return f'Transaction(id={self.id}, valuta={self.valuta}, debit={self.debit}, credit={self.credit}, value={self.value})'


def load_docs(path: pathlib.Path) -> typing.List[Document]:
    """
    Load the PDF documents at the specified path
    Args:
        path (pathlib.Path): The path to the folder containing the PDF documents

    Returns:
        A list of Langchain Document objects
    """
    loader = PyPDFDirectoryLoader(path,
                                  glob="**/*.pdf",
                                  mode='single',
                                  extraction_mode='layout')
    return loader.load()

def main() -> int:
    parser = argparse.ArgumentParser(description=f'mrmat-finance-pdf-parser - {__version__}')
    parser.add_argument('--path',
                        type=pathlib.Path,
                        required=True,
                        dest='path',
                        help='Path to the folder containing financial statements')
    parser.add_argument('--db-url',
                        type=str,
                        required=True,
                        dest='db_url',
                        help='The database URL, in the format postgresql+psycopg2://USER:PASS@HOST/DB')
    parser.add_argument('--model',
                        type=str,
                        required=False,
                        choices=['gpt-oss:20b', 'gemma3:27b'],
                        default='gpt-oss:20b',
                        dest='model',
                        help='The model to use for the LLM')
    args = parser.parse_args()
    engine = db(args.db_url)

    pdfs = load_docs(args.path)
    system_prompt = f"""
    You are an expert extraction algorithm for financial documents written in German. Only
    extract relevant information from the text.
    """
    llm = ChatOllama(model=args.model,
                     validate_model_on_init=True,
                     temperature=0.0).with_structured_output(schema=Statement,
                                                             method='json_schema',
                                                             include_raw=True)
    for pdf in pdfs:
        try:
            print(f"- Parsing document {pdf.metadata.get('source')}")
            response = llm.invoke([SystemMessage(content=system_prompt),
                                   HumanMessage(content=pdf.page_content)])
            if response['parsing_error']:
                print(f"ERROR: Failed to parse document {pdf.metadata.get('source')}: {response['parsing_error']}")
                continue
            parsed = response['parsed']
            with Session(engine) as session:
                for tx in parsed.transactions:
                    ormtx = ORMTransaction.from_parsed(parsed.iban, tx)
                    session.add(ormtx)
                session.commit()
        except ValidationError as ve:
            print(f"ERROR: Failed to parse document {pdf.metadata.get('source')}: {ve}")
        except SQLAlchemyError as se:
            print(f"Database error: Failed to update database: {se}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
