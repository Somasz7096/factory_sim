from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from .engine import engine


class Base(DeclarativeBase):
    pass


def warehouse_factory(table_name: str, class_name: str):
    class Warehouse(Base):
        __tablename__ = table_name

        material_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        name: Mapped[str]
        details: Mapped[str]
        supplier: Mapped[int]

        def __repr__(self):
            return f"[{self.material_id}]: {self.name}, {self.details}, {self.supplier}"

    Warehouse.__name__ = class_name
    Warehouse.__qualname__ = class_name
    Warehouse.__module__ = __name__
    return Warehouse


Warehouse_1000 = warehouse_factory("warehouse_1000", "Warehouse1000")
Warehouse_1100 = warehouse_factory("warehouse_1100", "Warehouse1100")

class Item(Base):
    __tablename__ = "items"

    index: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    volume: Mapped[str] = mapped_column(String(10), nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False)
    items_per_cycle: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"[{self.index}]: {self.type}, {self.volume}, {self.color}, {self.items_per_cycle}"

    __table_args__ = (
        UniqueConstraint('type', 'volume', 'color', name="xxx"),
    )



class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(Integer)
    item_index: Mapped[str] = mapped_column(ForeignKey("items.index"))


Base.metadata.create_all(engine)