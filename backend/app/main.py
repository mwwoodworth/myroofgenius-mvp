from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session

app = FastAPI(
    title="MyRoofGenius API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS configuration
origins = ["*"]  # Update for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str


@app.get("/healthz", response_model=HealthResponse)
async def healthz():
    return {"status": "ok"}


DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./local.db"  # Fallback for local dev
)
engine = create_engine(DATABASE_URL, echo=False)


class Lead(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


SQLModel.metadata.create_all(engine)


class LeadIn(BaseModel):
    name: str
    email: str
    message: str


@app.post("/leads", status_code=status.HTTP_201_CREATED)
async def create_lead(lead: LeadIn):
    with Session(engine) as session:
        db_lead = Lead.model_validate(lead, from_attributes=True)
        session.add(db_lead)
        session.commit()
        session.refresh(db_lead)
        return db_lead
