from datetime import datetime as dt
from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL
from .base import Base


class Node(Base):
    """
    Node Model
    """

    __tablename__ = 'nodes'

    Id = Column(Integer(), primary_key=True)
    Ip = Column(String(15), nullable=False)
    Consumption = Column(DECIMAL(precision=10, scale=8), nullable=False)
    Timestamp = Column(TIMESTAMP(), nullable=False, default=dt.now())

    def serialize(self):
        """
        Serialize the data

        Returns:
            dict: The serialized data
        """

        return {
            "Id": self.Id,
            "Ip": self.Ip,
            "Consumption": self.Consumption,
            "Timestamp": self.Timestamp,
        }
