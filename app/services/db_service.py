

from app.utils.energyplan import parse_single_rate, parse_tariff_period


async def fetch_single_rate(db):
    plans_collection = db["plans"]
    document = await plans_collection.find_one(
        {"_id": "NTR823818MRE1@EME"})
    if document and "electricity_contract" in document:
        # Extract single_rate from the first tariff period (adjust if needed)
        single_rate_data = document['electricity_contract']['tariff_period'][0].get(
            'single_rate')

        if single_rate_data:
            return parse_single_rate(single_rate_data)
    return None


async def fetch_tariff_period(db):
    plans_collection = db["plans"]
    document = await plans_collection.find_one(
        {"_id": "NTR823818MRE1@EME"})
    if document and "electricity_contract" in document:
        # Extract single_rate from the first tariff period (adjust if needed)
        tariff_period_data = document['electricity_contract'].get(
            'tariff_period')[0]

        if tariff_period_data:
            return parse_tariff_period(tariff_period_data)
    return None
