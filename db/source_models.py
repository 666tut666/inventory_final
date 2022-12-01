from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime,
                        ForeignKey, Integer, String)
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    phone = Column(String(50))
    creation_date = Column(DateTime)
    activation_date = Column(DateTime, nullable=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    status_type_id = Column(Integer, ForeignKey("status_type.id"))

    employer = relationship(
        "Employer",
        uselist=False,
        single_parent=True,
        backref="user",
        passive_deletes=True,
    )
    employee = relationship(
        "Employee",
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


class Employer(Base):
    __tablename__ = "employer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    address = Column(String(100))
    edrpou = Column(String(50), index=True)
    expire_contract_date = Column(Date, nullable=True)
    salary_date = Column(Date, nullable=True)
    prepayment_date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    employer_type_id = Column(Integer, ForeignKey("employer_type.id"))

    employees = relationship(
        "Employee",
        backref="employer",
    )
    employer_payment_methods = relationship(
        "EmployerPaymentMethod",
        backref="employer",
        passive_deletes=True,
    )


class EmployerType(Base):
    __tablename__ = "employer_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)

    employers = relationship("Employer", backref="employer_type")


class EmployerPaymentMethod(Base):
    __tablename__ = "employer_payment_method"

    id = Column(Integer, primary_key=True, index=True)
    iban = Column(String(50))
    is_active = Column(Boolean, default=False)
    creation_date = Column(DateTime)
    deactivation_date = Column(Date)
    employer_id = Column(Integer, ForeignKey("employer.id", ondelete="CASCADE"))
    bank_id = Column(Integer, ForeignKey("bank.id", ondelete="CASCADE"))

    payment_histories = relationship(
        "PaymentHistory",
        backref="employer_payment_method",
    )


class Bank(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    mfo = Column(String(50))
    is_active = Column(Boolean, default=False)
    creation_date = Column(DateTime)
    deactivation_date = Column(Date)

    employer_payment_method = relationship(
        "EmployerPaymentMethod",
        backref="bank",
        passive_deletes=True,
    )


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100))
    passport = Column(String(50), index=True, nullable=True)
    tax_id = Column(String(50), index=True, nullable=True)
    birth_date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    employer_id = Column(Integer, ForeignKey("employer.id"))

    employee_accounts = relationship(
        "EmployeeAccount",
        backref="employee",
        passive_deletes=True,
    )


class EmployeeAccount(Base):
    __tablename__ = "employee_account"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    number = Column(String(50))
    is_active = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False)
    issuer = Column(String(100))
    creation_date = Column(DateTime)
    deactivation_date = Column(Date)
    employee_id = Column(Integer, ForeignKey("employee.id", ondelete="CASCADE"))
    account_type_id = Column(Integer, ForeignKey("account_type.id"))

    payment_histories = relationship(
        "PaymentHistory",
        backref="employee_account",
    )


class AccountType(Base):
    __tablename__ = "account_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    employee_accounts = relationship(
        "EmployeeAccount",
        backref="account_type",
    )


class PaymentHistory(Base):
    __tablename__ = "payment_history"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(BigInteger)
    creation_date = Column(DateTime)
    employee_account_id = Column(
        Integer, ForeignKey("employee_account.id")
    )
    employer_payment_method_id = Column(
        Integer, ForeignKey("employer_payment_method.id")
    )
    payment_status_type_id = Column(
        Integer, ForeignKey("payment_status_type.id")
    )


class PaymentStatusType(Base):
    __tablename__ = "payment_status_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    payment_histories = relationship(
        "PaymentHistory",
        backref="payment_status_type",
    )
