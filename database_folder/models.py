from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
try:
    from engine import engine
except:
    from .engine import engine


class Base(DeclarativeBase):
    pass



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