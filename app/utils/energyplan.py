from app.models.tariff_period_model import ERate, ERateSingle, SingleRate, TariffPeriod


def parse_erate(rates: list) -> ERate:
    """
    Examlpe input:
    "rates": [
        {
            "measure_unit": "KWH",
            "unit_price": "0.3045",
            "volume": 0
        },
        {
            "unit_price": "0.35",
            "volume": 11
        }
    ]

    Parameters
    ----------
    rates : list
        A list of rates.

    Returns
    -------
    eplan_models.ERate
    """
    rate_recods = []

    for rate in rates:
        measure_unit = 'kwh'
        unit_price = None
        volume = 0.0
        # volume_price = 0.0
        measure_unit_tmp = rate.get("measure_unit", None)
        if measure_unit_tmp is not None:
            measure_unit = measure_unit_tmp.strip().lower()

        volume = rate.get("volume", 0.0)
        unit_price = rate['unit_price']
        # TODO need to check measure_unit and convert to correct unit
        measure_unit = 'kwh'
        erate_single = ERateSingle(
            measure_unit=measure_unit,
            unit_price=unit_price,
            volume=volume
        )
        rate_recods.append(erate_single)
    erate = ERate(rates=rate_recods)
    return erate


def parse_single_rate(data: dict) -> SingleRate:
    """
    Example input:
    {
        "display_name": "General Usage",
        "period": "PT24H",
        "rates": check parse_erate()
    }

    Parameters
    ----------
    data : dict
        A dictionary containing the data for the single rate.

    Returns
    -------
    eplan_models.SingleRate
    """
    description = data.get("description", None)
    display_name = data.get("display_name", None)
    general_unit_price = data.get("general_unit_price", None)

    raw_period = data.get("period", None)
    period = raw_period

    rates = data.get("rates", None)
    if rates is None:
        rates = []
    rate = parse_erate(rates)

    daily_supply_charge = data.get("daily_supply_charge", 0)

    single_rate = SingleRate(
        description=description,
        display_name=display_name,
        general_unit_price=general_unit_price,
        period=period,
        rate=rate,
        daily_supply_charge=daily_supply_charge
    )
    return single_rate


def parse_tariff_period(data: dict) -> TariffPeriod:
    """
    "tariff_period": [input_data, input_data, ...]

    Parameters
    ----------
    data : dict
        A dictionary containing the data for the tariff period.

    Returns
    -------
    eplan_models.TariffPeriod
    """
    display_name = data.get("display_name", None)
    start_date = data.get("start_date", None)
    end_date = data.get("end_date", None)
    daily_supply_charge = data.get("daily_supply_charges", 0)

    time_zone = data.get("time_zone", None)
    charge_type = data.get("type", None)

    single_rate = None

    raw_single_rate = data.get("single_rate", None)
    if raw_single_rate is not None:
        single_rate = parse_single_rate(raw_single_rate)

    tariff_period = TariffPeriod(
        display_name=display_name,
        start_date=start_date,
        end_date=end_date,

        daily_supply_charge=daily_supply_charge,

        single_rate=single_rate,

        time_zone=time_zone,
        charge_type=charge_type
    )
    return tariff_period
