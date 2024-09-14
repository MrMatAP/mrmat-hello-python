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

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from mhpython.ddd.base import DDDModel


class NetworkModel(DDDModel):
    __tablename__ = 'networks'
    network: Mapped[str] = mapped_column(String(15))
    netmask: Mapped[str] = mapped_column(String(15))
    router: Mapped[str] = mapped_column(String(15))

class ImageModel(DDDModel):
    __tablename__ = 'images'
    url: Mapped[str] = mapped_column(String(15))
    path: Mapped[str] = mapped_column(String(15))

class ClusterModel(DDDModel):
    __tablename__ = 'clusters'

class NodeModel(DDDModel):
    __tablename__ = 'nodes'
    network_uid: Mapped[str] = mapped_column(ForeignKey("networks.uid"))
    image_uid: Mapped[str] = mapped_column(ForeignKey("images.uid"))
    cluster_uid: Mapped[str] = mapped_column(ForeignKey("clusters.uid"), nullable=True)

    network: Mapped[NetworkModel] = relationship(lazy='selectin')
    image: Mapped[ImageModel] = relationship(lazy='selectin')
    cluster: Mapped[ClusterModel] = relationship(lazy='selectin')
