from datetime import datetime as dt
from sqlalchemy import Column, Integer, TIMESTAMP, DECIMAL
from .base import Base


class Speed(Base):
    """
    Speed Model
    """

    __tablename__ = 'speeds'

    Id = Column(Integer(), primary_key=True)
    Speed = Column(DECIMAL(precision=10, scale=8), nullable=False)
    Timestamp = Column(TIMESTAMP(), nullable=False, default=dt.now())

    def serialize(self):
        """
        Serialize the data

        Returns:
            dict: The serialized data
        """

        return {
            "Id": self.Id,
            "Speed": self.Speed,
            "Timestamp": self.Timestamp,
        }
