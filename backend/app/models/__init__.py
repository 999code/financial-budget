"""集中导出所有 ORM 模型，确保 create_all 时能注册全部表。"""
from app.models.user import User
from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.budget import Budget
from app.models.income_expense import IncomeExpense
from app.models.income_expense_detail import IncomeExpenseDetail
from app.models.loan import Loan
from app.models.pension import Pension, PensionParams, PensionPerson

__all__ = [
    "User",
    "Account",
    "Category",
    "Transaction",
    "Budget",
    "IncomeExpense",
    "IncomeExpenseDetail",
    "Loan",
    "Pension",
    "PensionParams",
    "PensionPerson",
]
