import os
import datetime
import logging
from .utils import get_cache_dir, get_product_url

logger = logging.getLogger(__name__)

_max_forecast_hours = {
    "icon-eu": 120,
    "icon-d2": 48,
    "icon-global": 120,  # TODO check this value
}


class Forecast:
    def __init__(
        self,
        start_datetime: str,
        end_datetime: str,
        dwd_product: str = "icon-eu",
    ) -> None:
        try:
            self.start_datetime = datetime.datetime.fromisoformat(start_datetime)
            self.end_datetime = datetime.datetime.fromisoformat(end_datetime)
        except BaseException as e:
            logger.error(
                f"Could not convert start-/end-datetime into datetime object."
                f"Both must be provided in ISO 8601 dateformat"
                f"Error: {e}"
            )
            raise e
        if self.start_datetime > self.end_datetime:
            raise ValueError("Start datetime must be before end datetime")
        logger.info(
            f"Forecast object created with start_datetime: {self.start_datetime} "
            f"and end_datetime: {self.end_datetime}"
        )

        self._cache_dir = os.path.join(
            get_cache_dir(),
            "forecasts",
            datetime.datetime.now().strftime("%Y-%m-%d_%H"),
        )
        if not os.path.exists(self._cache_dir):
            os.makedirs(self._cache_dir)
            logger.info(f"Created cache directory: {self._cache_dir}")

        self._product_url = get_product_url(dwd_product)
        self._max_forecast_hours = _max_forecast_hours[dwd_product]
        self._forecast_duration = int((self.end_datetime - self.start_datetime).total_seconds() // 3600)

        if self.start_datetime - datetime.datetime.now() > datetime.timedelta(hours=self._max_forecast_hours):
            raise ValueError(
                "Start datetime is too far in the future. "
            )
        if datetime.datetime.now() - self.start_datetime > datetime.timedelta(hours=self._max_forecast_hours):
            raise ValueError(
                "Start datetime is too far in the past. "
            )

        if self._forecast_duration > self._max_forecast_hours:
            logger.warning(
                f"Forecast duration ({self._forecast_duration}h) exceeds maximum forecast duration"
                f"({self._max_forecast_hours}h) for product {dwd_product}."
                f" Only the first {self._max_forecast_hours} hours will be downloaded."
            )
            self._forecast_duration = self._max_forecast_hours

    def __repr__(self) -> str:
        return f"Forecast(start_datetime={self.start_datetime}, end_datetime={self.end_datetime})"

    def get_data(self) -> None:
        # TODO implement here to download most recent forecast data.
        # for this one will need to use some logic to first find the most recent simulation-run for each forecast-hour
        # and then download the corresponding grib file if it does not exist in the cache directory
        pass
