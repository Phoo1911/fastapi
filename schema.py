from pydantic import BaseModel

class Transaction(BaseModel):
    amount: float
    type: str
    description: str

    class Config:
        # Use this in Pydantic V2
        from_attributes = True

