from src.main.api.models.base_model import BaseModel


class CreateCreditResponse(BaseModel):
    id: int
    amount: float | int
    termMonths: int
    balance: float | int
    creditId: int