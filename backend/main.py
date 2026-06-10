from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.graph import build_graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()


# -----------------------------
# REQUEST MODEL
# -----------------------------

class ProfileInput(BaseModel):
    age: int
    income: float
    years: int
    loss: int
    amount: float


# -----------------------------
# GENERATE ROUTE
# -----------------------------

@app.post("/generate")
def generate(profile: ProfileInput):

    try:
        initial_state = {
            "profile": profile.dict(),
            "logs": [],
            "retry": False
        }

        result = graph.invoke(initial_state)

        # Return only structured output
        return {
            "risk_score": result.get("risk_score"),
            "allocation": result.get("allocation"),
            "stress_test": result.get("stress_test"),
            "explanation": result.get("explanation"),
            "compliance": result.get("compliance_review"),
            "logs": result.get("logs")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))