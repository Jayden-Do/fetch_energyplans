import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse


from app.dependencies import get_database
from app.services.db_service import fetch_tariff_period
from app.services.fiskil_service import get_detail_energy_plan, get_energy_plan_by_retailer

app = FastAPI()

load_dotenv()


@app.get("/plans_by_retailer/{retailer_id}")
async def fetch_plans_by_retailer_from_fiskil(retailer_id: str):
    """
    Fetch data from Fiskil API using the access token.
    """
    plans, status_code = await get_energy_plan_by_retailer(retailer_id)

    if plans is not None:
        return plans
    else:
        raise HTTPException(
            status_code=status_code,
            detail="Failed to fetch plans"
        )


@app.get("/detail_plan/{plan_id}")
async def fetch_detail_plan_from_fiskil(plan_id: str):
    """
    Fetch data from Fiskil API using the access token.
    """
    data, status_code = await get_detail_energy_plan(plan_id)

    if data is not None:
        return data
    else:
        raise HTTPException(
            status_code=status_code,
            detail="Failed to fetch plans"
        )


@app.get("/plans/tariff_period")
async def get_tariff_period(db=Depends(get_database)):
    """
    API endpoint to fetch single_rate for a given plan_id.
    """
    tariff_period = await fetch_tariff_period(db)

    if tariff_period is None:
        raise HTTPException(status_code=404, detail="Single rate not found")

    return tariff_period
