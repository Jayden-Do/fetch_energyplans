from typing import Optional
from pydantic import BaseModel, Field


class ERateSingle(BaseModel):
    measure_unit: str | None = "kwh"
    unit_price: float = Field(
        ..., description="price of usage per measure unit 'exclusive of gst'")
    volume: float = 0.0


class ERate(BaseModel):
    rates: list[ERateSingle]


class SingleRate(BaseModel):
    description: Optional[str] = None
    display_name: Optional[str] = None
    general_unit_price: Optional[float] = Field(
        None,
        description="general_unit_price the block rate \
            (unit price) for any usage above the included \
            fixed usage, in dollars per k_wh 'inclusive of gst'. \
            only required if pricing_model field is quota")
    period: Optional[str] = Field(
        None,
        description="ISO 8601 durations format")
    rate: ERate
    daily_supply_charge: Optional[float] = Field(
        0,
        description="apply for controlled_load only, \
            dollars per day 'exclusive of gst'")


class TariffPeriod(BaseModel):
    display_name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    daily_supply_charge: Optional[float] = Field(
        0,
        description="in dollars per day 'exclusive of gst'")
    single_rate: Optional[SingleRate] = None
    time_zone: Optional[str] = None
    charge_type: Optional[str] = None
