
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

try:
    from .engine import SessionLocal
    from .models import Item, Order
except:
        from engine import SessionLocal
        from models import Item, Order


session = SessionLocal()

# items_to_add = (
#     {"type": "pojemnik", "volume": "0,5l", "color": "biały", "items_per_cycle": 80},
#     {"type": "pojemnik", "volume": "0,5l", "color": "zielony", "items_per_cycle": 80},
#     {"type": "pojemnik", "volume": "0,5l", "color": "żółty", "items_per_cycle": 80},
#     {"type": "pojemnik", "volume": "0,5l", "color": "czerwony", "items_per_cycle": 80},
#     {"type": "pojemnik", "volume": "1l", "color": "biały", "items_per_cycle": 70},
#     {"type": "pojemnik", "volume": "1l", "color": "zielony", "items_per_cycle": 70},
#     {"type": "pojemnik", "volume": "1l", "color": "żółty", "items_per_cycle": 70},
#     {"type": "pojemnik", "volume": "1l", "color": "czerwony", "items_per_cycle": 70},
#     {"type": "pojemnik", "volume": "2l", "color": "biały", "items_per_cycle": 60},
#     {"type": "pojemnik", "volume": "2l", "color": "zielony", "items_per_cycle": 60},
#     {"type": "pojemnik", "volume": "2l", "color": "żółty", "items_per_cycle": 60},
#     {"type": "pojemnik", "volume": "2l", "color": "czerwony", "items_per_cycle": 60},
#     {"type": "pojemnik", "volume": "5l", "color": "biały", "items_per_cycle": 30},
#     {"type": "pojemnik", "volume": "5l", "color": "zielony", "items_per_cycle": 30},
#     {"type": "pojemnik", "volume": "5l", "color": "żółty", "items_per_cycle": 30},
#     {"type": "pojemnik", "volume": "5l", "color": "czerwony", "items_per_cycle": 30},
#
# )
#
#
# for data in items_to_add:
#     session.add(Item(**data))
#     try:
#         session.commit()
#     except IntegrityError:
#         session.rollback()
#         print(f"{data} already exists")

def _print_results():
    results = session.scalars(select(Item)).all()
    for r in results:
        print(r)




def save(record):
    try:
        session.add(record)
        session.commit()
        _print_results()
        print(f"{record} added")
    except IntegrityError:
        session.rollback()
        print(f"{record} already exists")

    except Exception as e:
        print(f"save to db error - {e}")
    session.close()

def load(index: str, model):
    try:
        result = session.scalar(select(model).where(model.index == index))
        return result
    except Exception as e:
        print(e)

