from fastapi import Depends
from httpx import AsyncClient
import asyncio
import os
from dotenv import load_dotenv
# from pymongo import InsertOne

import app.utils.constants as constants

# Load environment variables
load_dotenv()

# Constants
FISKIL_CLIENT_ID = os.getenv("FISKIL_CLIENT_ID")
FISKIL_CLIENT_SECRET = os.getenv("FISKIL_CLIENT_SECRET")
FISKIL_API_URL = os.getenv("FISKIL_API_URL")
FISKIL_AUTH_ENDPOINT = os.getenv("FISKIL_AUTH_ENDPOINT")
FISKIL_PLANS_ENDPOINT = os.getenv("FISKIL_PLANS_ENDPOINT")

# In-memory cache to store plan details (optional)
cache = {}

# MongoDB setup
# from dependencies import mongo_db  # Assuming you have set up mongo_db in a dependencies file

# Get access token from Fiskil


async def get_access_token():
    url = FISKIL_API_URL + FISKIL_AUTH_ENDPOINT
    data = {
        "client_id": FISKIL_CLIENT_ID,
        "client_secret": FISKIL_CLIENT_SECRET,
    }
    async with AsyncClient(timeout=60.0) as client:
        response = await client.post(url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            return token_data['token']
        else:
            raise Exception("Failed to retrieve access token")

# Fetch all plans by retailer_id (with pagination support)


async def get_energy_plan_by_retailer(retailer_id: str):
    url = FISKIL_API_URL + FISKIL_PLANS_ENDPOINT + \
        f'?retailer_id={retailer_id}'
    access_token = await get_access_token()
    async with AsyncClient(timeout=60.0) as client:
        response = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
        status_code = response.status_code
        if status_code == 200:
            plans = response.json()
            return plans, status_code
        else:
            raise Exception(
                f"Failed to retrieve plans for retailer {retailer_id}")

# Fetch plan details by plan_id (with caching)


async def get_detail_energy_plan(energy_plan_id):
    # Check cache first to avoid redundant requests
    if energy_plan_id in cache:
        return cache[energy_plan_id]

    url = FISKIL_API_URL + FISKIL_PLANS_ENDPOINT + f'/{energy_plan_id}'
    access_token = await get_access_token()
    async with AsyncClient(timeout=60.0) as client:
        response = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
        status_code = response.status_code
        if status_code == 200:
            data = response.json()
            cache[energy_plan_id] = data  # Cache the result
            return data
        else:
            raise Exception(
                f"Failed to retrieve details for plan {energy_plan_id}")

# Fetch plan details concurrently using asyncio.gather


async def get_detail_energy_plans_concurrently(plan_ids):
    tasks = [get_detail_energy_plan(plan_id) for plan_id in plan_ids]
    results = await asyncio.gather(*tasks)
    return results

# # Save all fetched plans to MongoDB in bulk
# async def save_plans_to_db(plans):
#     requests = [InsertOne(plan) for plan in plans]
#     await mongo_db.collection.bulk_write(requests)

# Main function to fetch all plans for multiple retailers


async def get_all_plans(limit: int = 50):
    all_plans = []
    count = 0
    for retailer_id in constants.retailer_ids.split():
        page = 20
        while True:
            data, _ = await get_energy_plan_by_retailer(retailer_id)
            plan_list = data.get("plans", [])

            if not plan_list:
                break  # No more plans to fetch

            # Fetch plan details concurrently
            plan_ids = [plan["plan_id"] for plan in plan_list]
            plan_details = await get_detail_energy_plans_concurrently(plan_ids)

            all_plans.extend(plan_details)

            count += len(plan_details)
            if count >= limit:  # Stop once the limit is reached
                return all_plans

            page += 1

    return all_plans
