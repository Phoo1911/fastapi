from fastapi import FastAPI, Form, Request, Depends, HTTPException
from sqlalchemy.orm import Session
import crud,  database
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Initialize FastAPI and database
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the database (only once)
@app.on_event("startup")
def startup():
    database.init_db()

# Home route - Display transactions
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db)
    return templates.TemplateResponse("index.html", {"request": request, "transactions": transactions})

# Add transaction
@app.post("/add_transaction")
async def add_transaction(request: Request, amount: float = Form(...), transaction_type: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    transaction = crud.add_transaction(db, amount, transaction_type, description)
    return templates.TemplateResponse("index.html", {"request": request, "transactions": crud.get_transactions(db), "message": "Transaction added successfully!"})

# Delete transaction
@app.post("/delete_transaction/{transaction_id}")
async def delete_transaction(request: Request, transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.delete_transaction(db, transaction_id)
    if transaction:
        return templates.TemplateResponse("index.html", {"request": request, "transactions": crud.get_transactions(db), "message": "Transaction deleted successfully!"})
    raise HTTPException(status_code=404, detail="Transaction not found")
