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

import pydantic
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from sqlalchemy import String, DateTime, Float, ForeignKey

from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFDirectoryLoader

from mhpython import __version__

class Transaction(BaseModel):
    """
    An individual transaction. Ignore any transaction that has an empty 'Datum' or where the 'Information'
    field only contains 'Anfangssaldo'. Note that the 'Information' field has multiple lines.
    """
    date: typing.Optional[datetime.datetime] = Field(description="The 'Datum' date of the transaction")
    counterparty: typing.Optional[str] = Field(description="The 'Information' of the transaction, as a multiline string")
    debit: typing.Optional[float] = Field(description="The 'Belastungen' of the transaction, or 0 when empty", default=0)
    credit: typing.Optional[float] = Field(description="The 'Gutschriften' of the transaction, or 0 when empty", default=0)
    valuta: typing.Optional[datetime.datetime] = Field(description="The 'Valuta' date of the transaction")
    value: typing.Optional[float] = Field(description="The 'Kontostand' of the transaction", default=0)

class Statement(BaseModel):
    """Information about a statement"""
    iban: str = Field(description="The value of the IBAN field on the first page of the document")
    created_at: typing.Optional[datetime.datetime] = Field(description="The value of the 'Erstellt am' field on the first page of the document")
    value_start: typing.Optional[float] = Field(description="The 'Anfangssaldo' in the 'Ihr Konto auf einen Blick' section")
    total_credit: typing.Optional[float] = Field(description="The 'Gutschriften' in the 'Ihr Konto auf einen Blick' section")
    total_debit: typing.Optional[float] = Field(description="The 'Belastungen' in the 'Ihr Konto auf einen Blick' section")
    value_end: typing.Optional[float] = Field(description="The 'Schlusssaldo' in the 'Ihr Konto auf einen Blick' section")
    transactions: typing.List[Transaction] = Field(default_factory=list, title="One entry for each transaction following the 'Ihr Konto auf einen Blick' section")

class Account(BaseModel):
    """Information about an accoun"""
    iban: str = Field(description="IBAN")
    statements: typing.List[Statement] = Field(description="Statements", default_factory=list)

class ORMBase(DeclarativeBase):
    pass

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

def db(url: str) -> Engine:
    """
    Connect to the database and ensure all tables are created
    Args:
        url: The database URL in the format postgresql+psycopg2://USER:PASSWORD@HOST/DATABASE

    Returns:
        The database engine
    """
    engine = create_engine(url, echo=True)
    ORMBase.metadata.create_all(engine)
    return engine

def docs(path: pathlib.Path) -> typing.List[Document]:
    loader = PyPDFDirectoryLoader(path,
                                  glob="**/*.pdf",
                                  mode='single',
                                  extraction_mode='layout')
    return loader.load()

def main() -> int:
    parser = argparse.ArgumentParser(description=f'mrmat-finance - {__version__}')
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
    args = parser.parse_args()
    engine = db(args.db_url)

    statements = docs(args.path)
    pydantic_parser = PydanticOutputParser(pydantic_object=Statement)
    system_prompt = f"""
    You are an expert extraction algorithm for financial documents written in German. Only
    extract relevant information from the text.
    
    Wrap the output in JSON \n{pydantic_parser.get_format_instructions()}
    """
    # This fails with 'dict object has no attributed 'content''. there's somee incompatibility here
    #llm = ChatOllama(model="gpt-oss:20b",
    #                validate_model_on_init=True).with_structured_output(schema=Statement, include_raw=True)
    llm = ChatOllama(model="gpt-oss:20b", validate_model_on_init=True)
    for statement in statements:
        print(f"- Parsing document {statement.metadata.get('source')}")
        response = llm.invoke([SystemMessage(content=system_prompt),
                               HumanMessage(content=statement.page_content)])
        try:
            parsed = pydantic_parser.parse(response.content)
            with Session(engine) as session:
                for tx in parsed.transactions:
                    ormtx = ORMTransaction.from_parsed(parsed.iban, tx)
                    session.add(ormtx)
                session.commit()
        except pydantic.ValidationError | ValueError as ve:
            print(f"ERROR: Failed to parse document {statement.metadata.get('source')}: {ve}")
        except SQLAlchemyError as se:
            print(f"Database error: Failed to update database: {se}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
