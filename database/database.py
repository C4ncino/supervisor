"""
Database Interface Class
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc
from dotenv import load_dotenv

from .base import Base
from .node import Node
from .speed import Speed

load_dotenv()

TABLE_CLASS_MAP = {
    'nodes': Node,
    'speeds': Speed
}


class DatabaseInterface:
    """
    DB Interface with SQLAlchemy and PostgreSQL
    """

    def __init__(self) -> None:
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_port = os.getenv('DB_PORT')
        db_host = os.getenv('DB_HOST')

        self.db_url = "postgresql://"
        self.db_url += f"{db_user}:{db_password}"
        self.db_url += f"@{db_host}:{db_port}/{db_name}"

        self.engine = create_engine(self.db_url, echo=False)

        session_class = sessionmaker(bind=self.engine)

        self.session = session_class()

        Base.metadata.create_all(self.engine)

    def create_table_row(self, table_name: str, row_info: dict):
        """
        Create a new row in the table

        Args:
            table_name: The name of the table
            row_info: The info of the row

        Returns:
            bool: True if the row was created, False otherwise
        """

        table_class = TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            row = table_class(**row_info)
            self.session.add(row)
            self.session.commit()

            return True, row

        return False, None

    def read_all_table(self, table_name):
        """
        Read all rows in the table
        """

        table_class = TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            data = self.session.query(table_class).all()

            return data if len(data) > 0 else []

        return []

    def read_by_id(self, table_name, element_id):
        """
        Read a row by id

        Args:
            table_name: The name of the table
            element_id: The id of the element

        Returns:
            object: The row
        """

        table_class = TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            data = self.session.query(table_class)

            return data.filter(table_class.Id == element_id).first()

        return None

    def read_by_field(self, table_name, field, value):
        """
        Read all rows by a selected field

        Args:
            table_name: The name of the table
            field: The name of the field
            value: The field value

        Returns:
            object: The row
        """

        table_class = TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            data = self.session.query(table_class)
            data = data.filter(
                    getattr(table_class, field) == value
                ).all()

            return data if len(data) > 0 else []

        return []

    def update_table_row(self, table_name, element_id, row_info):
        """
        Update a row by id

        Args:
            table_name: The name of the table
            element_id: The id of the element
            row_info: The info of the row

        Returns:
            object: The row
        """

        table_class = TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            data = self.session.query(table_class)
            data = data.filter(table_class.Id == element_id).first()

            for key, value in row_info.items():
                setattr(data, key, value)
            self.session.commit()

            return data

        return None

    def delete_table_row(self, table_name, id_element):
        """
        Delete a row by id

        Args:
            table_name: The name of the table
            id_element: The id of the element

        Returns:
            bool: True if the row was deleted, False otherwise
        """

        table_class = TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            try:
                data = self.session.query(table_class)
                data = data.filter(table_class.Id == id_element).first()

                self.session.delete(data)
                self.session.commit()

            except sqlalchemy.exc.SQLAlchemyError as e:
                return False, e

            return True

        return False

    def update_hosts(self, ips):
        nodes = self.read_all_table('nodes')

        for node in nodes:
            if node.Ip in ips:
                node.Ip = True

                ips.remove(node.Ip)

            elif node.Ip not in ips:
                node.Ip = False

        self.session.commit()

        return ips
