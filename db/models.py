from db.database import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    creation_date = Column(Date)
    #activation_date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    status_type_id = Column(Integer, ForeignKey("status_type.id"))
    role_id= Column(Integer, ForeignKey("role.id"))

    admin = relationship(
        "Admin",
        uselist=False,
        single_parent=True,
        backref="user",
        passive_deletes=True,
    )
    sessions = relationship(
        "Session",
        backref="user",
        passive_deletes=True,
    )


class StatusType(Base):
    __tablename__ = "status_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)

    users = relationship("User", backref="status_type")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)

    users = relationship("User", backref="role")


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(400))
    creation_date = Column(DateTime)
    status = Column(String(50))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    admin_type_id = Column(Integer, ForeignKey("admin_type.id"))

#class Ad


class AdminType(Base):
    __tablename__ = "admin_type"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)

    admins = relationship("Admin", backref="admin_type")



class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    item_type = Column(String)
    category = Column(String)
    quantity= Column(Integer)
    creation_date = Column(Date)


class Pending(Base):
    __tablename__ = "pending"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    item_type = Column(String)
    category = Column(String)
    quantity = Column(Integer)
    email = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    admin_id = Column(Integer, ForeignKey("admin.id"))



'''
## Trying new method for pending, allowed, taken and returned
    
    class Order(Base):
    
        ORDER_STATUSES=(
            ('PENDING','pending'),
            ('IN-TRANSIT','in-transit'),
            ('DELIVERED','delivered')
    
        )
    
        PIZZA_SIZES=(
            ('SMALL','small'),
            ('MEDIUM','medium'),
            ('LARGE','large'),
            ('EXTRA-LARGE','extra-large')
        )
    
    
        __tablename__='orders'
        id=Column(Integer,primary_key=True)
        quantity=Column(Integer,nullable=False)
        order_status=Column(ChoiceType(choices=ORDER_STATUSES),default="PENDING")
        pizza_size=Column(ChoiceType(choices=PIZZA_SIZES),default="SMALL")
        user_id=Column(Integer,ForeignKey('user.id'))
        user=relationship('User',back_populates='orders')
    
        def __repr__(self):
            return f"<Order {self.id}>"
'''
