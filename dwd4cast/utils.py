import os


def get_product_url(product: str) -> str:
    if product not in ["icon-eu", "icon-d2", "icon-global"]:
        raise NotImplementedError(f"Product {product} not supported (yet?)")
    return os.environ.get("DWD4CAST_PRODUCT_URL", f"https://opendata.dwd.de/weather/nwp/{product}/grib/")


def get_cache_dir() -> str:
    return os.environ.get("DWD4CAST_CACHE_DIR", os.path.join(os.path.expanduser("~"), ".dwd4cast"))
