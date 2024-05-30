from dwd4cast.forecast import Forecast
import os


def test_forecast_basic():
    forecast = Forecast("2024-05-30T20:00", "2024-05-31T20:00")
    assert forecast is not None


def test_forecast_invalid_datetime():
    try:
        _forecast = Forecast("2024-05-30T20:00", "2024-05-29T20:00")
    except ValueError as e:
        assert str(e) == "Start datetime must be before end datetime"


def test_forecast_delorean():
    try:
        _forecast = Forecast("2015-10-21T20:00", "2015-10-21T21:00")
    except ValueError as e:
        assert str(e) == "Start datetime is too far in the past. "


def test_forecast_cache_dir_exists():
    forecast = Forecast("2024-05-30T20:00", "2024-06-30T20:00")
    assert forecast._cache_dir is not None
    assert os.path.exists(forecast._cache_dir)


def test_forecast_product_url():
    forecast = Forecast("2024-05-30T20:00", "2024-05-30T22:00", dwd_product="icon-d2")
    assert forecast._product_url is not None
    assert forecast._product_url == "https://opendata.dwd.de/weather/nwp/icon-d2/grib/"
