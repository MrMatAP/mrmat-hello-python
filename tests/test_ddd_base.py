#  MIT License
#
#  Copyright (c) 2024 Mathieu Imfeld
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

import pytest
import uuid
import pydantic
#
# from sqlalchemy import UUID, String
# from sqlalchemy.orm import Mapped, mapped_column
#
# from mhpython.ddd_base.base_types import DDDMeta, DDDAttribute
# from mhpython.ddd_base.sample_person import DDDPersonSample
#
#
# class DDDPersonViaMeta(metaclass=DDDMeta):
#     __tablename__ = 'ddd_person'
#     id: uuid.UUID = DDDAttribute(
#         schema=pydantic.Field(default_factory=uuid.uuid4, description='A unique identity for this entity'),
#         orm=mapped_column(UUID(as_uuid=True).with_variant(String(32), 'sqlite'), primary_key=True))
#     name: str = DDDAttribute(
#         schema=pydantic.Field(description='The entity name'),
#         orm=mapped_column(String(30)))
#
#
# def test_ddd_person_via_meta():
#     """
#     Test that a class crafted via metaclass can be persisted and transformed
#     :return:
#     """
#     meta_person = DDDPersonViaMeta(name='MrMat')
#     assert meta_person.id is not None
#     assert meta_person.name == 'MrMat'
#
#
# @pytest.mark.skip
# @pytest.mark.asyncio
# async def test_ddd_person_sample(async_session_maker):
#     """
#     Test that a manually crafted class can be persisted and transformed
#     """
#     sample_person = DDDPersonSample(name='MrMat', session_maker=async_session_maker)
#     assert sample_person.id is not None
#     assert sample_person.name == 'MrMat'
#
#     persisted_person = await DDDPersonSample.get_by_id(id=sample_person.id, session_maker=async_session_maker)
#     assert sample_person.id == persisted_person.id
#     assert sample_person.name == persisted_person.name
