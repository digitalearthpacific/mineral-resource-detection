import dask.array as da
import joblib
import xarray as xr
from dask_ml.wrappers import ParallelPostFit
from datacube.utils.geometry import assign_crs

from xarray import Dataset
from pystac_client import Client
from odc.stac import load
import os

from planetary_computer import sign_url


DEP_CATALOG = "https://stac.staging.digitalearthpacific.org"
MSPC_CATALOG = "https://planetarycomputer.microsoft.com/api/stac/v1/"


def load_data(
    bbox: tuple[float],
    chunks: dict = dict(x=2048, y=2048),
    resolution: int = 10,
    datetime: str = "2023",
) -> Dataset:
    dep_client = Client.open("https://stac.staging.digitalearthpacific.org")
    collection = "dep_s2_geomad"

    items = list(
        dep_client.search(
            collections=[collection], bbox=bbox, datetime=datetime
        ).items()
    )

    bands = [
        "B02",
        "B03",
        "B04",
        "B05",
        "B06",
        "B07",
        "B08",
        "B8A",
        "B11",
        "B12",
        "emad",
        "bcmad",
        "smad",
    ]

    data = load(
        items,
        bbox=bbox,
        measurements=bands,
        resolution=resolution,
        chunks=chunks,
    ).squeeze("time")

    # Incorporate NDVI (Normalised Difference Vegetation Index) = (NIR-red)/(NIR+red)
    data["ndvi"] = (data["B08"] - data["B04"]) / (data["B08"] + data["B04"])

    # Incorporate MNDWI (Mean Normalised Difference Water Index) = (Green – SWIR) / (Green + SWIR)
    data["mndwi"] = (data["B03"] - data["B12"]) / (data["B03"] + data["B12"])

    # Incorporate EVI (Enhanced Vegetation Index) = 2.5NIR−RED(NIR+6RED−7.5BLUE)+1
    data["evi"] = (2.5 * (data["B08"] - data["B04"])) * (
        (data["B08"] + (6 * (data["B04"]) - (7.5 * (data["B02"]))))
    ) + 1

    # Incorporate SAVI (Standard Vegetation Index) = (800nm−670nm) / (800nm+670nm+L(1+L)) # where L = 0.5
    data["savi"] = (data["B07"] - data["B04"]) / (
        data["B07"] + data["B04"] + 0.5 * (1 + 0.5)
    )

    # Incorporate BSI (Bare Soil Index) = ((B11 + B4) - (B8 + B2)) / ((B11 + B4) + (B8 + B2)) # https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/barren_soil/
    data["bsi"] = ((data["B11"] + data["B04"]) - (data["B08"] + data["B02"])) / (
        (data["B11"] + data["B04"]) + (data["B08"] + data["B02"])
    )

    # Incorporate NDMI (Normalised Difference Moisture Index) # https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/ndmi/
    data["ndmi"] = ((data["B08"]) - (data["B11"])) / ((data["B08"]) + (data["B11"]))

    # Incorporate NDBI (Normalised Difference Built-up Index) (B06 - B05) / (B06 + B05); # - built up ratio of vegetation to paved surface - let BU = (ndvi - ndbi) - https://custom-scripts.sentinel-hub.com/custom-scripts/landsat-8/built_up_index/
    data["ndbi"] = ((data["B06"]) - (data["B05"])) / ((data["B06"]) + (data["B05"]))

    # TODO: rotate key and grab it from an actual environment variable
    os.environ["PC_SDK_SUBSCRIPTION_KEY"] = "84162f5502174b1b838239e74a44898d"

    mspc_client = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1/")

    # Get a pystac client for the MSPC
    items_dem = list(
        mspc_client.search(collections=["cop-dem-glo-30"], bbox=bbox).items()
    )

    data_dem = load(
        items_dem, chunks=chunks, groupby="solar_day", like=data, patch_url=sign_url
    )

    data_dem = (
        data_dem.where(data_dem != -32768).rename({"data": "elevation"}).squeeze("time")
    )

    data_s2_dem = data.update(data_dem)

    items_s1 = list(
        dep_client.search(
            collections=["dep_s1_mosaic"], bbox=bbox, datetime=datetime
        ).items()
    )
    data_s1 = load(
        items_s1,
        like=data,
        chunks=chunks,
        measurements=["mean_vv", "mean_vh"],
    ).squeeze("time")

    data_s1["mean_vv_vh"] = (data_s1["mean_vv"]) / (data_s1["mean_vh"])

    merged = data_s2_dem.update(data_s1)

    return merged


def predict_xr(
    model, input_xr, chunk_size=None, persist=False, proba=False, clean=False
):
    """
    Predict using a scikit-learn model on an xarray dataset.

    Shamelessly ripped from dea_tools
    """
    # if input_xr isn't dask, coerce it
    dask = True
    if not bool(input_xr.chunks):
        dask = False
        input_xr = input_xr.chunk({"x": len(input_xr.x), "y": len(input_xr.y)})

    # set chunk size if not supplied
    if chunk_size is None:
        chunk_size = int(input_xr.chunks["x"][0]) * int(input_xr.chunks["y"][0])

    def _predict_func(model, input_xr, persist, proba, clean):
        x, y, crs = input_xr.x, input_xr.y, input_xr.geobox.crs

        input_data = []

        variables = list(input_xr.data_vars)
        variables.sort()

        for var_name in variables:
            input_data.append(input_xr[var_name])

        input_data_flattened = []

        for arr in input_data:
            data = arr.data.flatten().rechunk(chunk_size)
            input_data_flattened.append(data)

        # reshape for prediction
        input_data_flattened = da.array(input_data_flattened).transpose()

        if clean is True:
            input_data_flattened = da.where(
                da.isfinite(input_data_flattened), input_data_flattened, 0
            )

        if (proba is True) & (persist is True):
            # persisting data so we don't require loading all the data twice
            input_data_flattened = input_data_flattened.persist()

        # apply the classification
        print("predicting...")
        out_class = model.predict(input_data_flattened)

        # Mask out NaN or Inf values in results
        if clean is True:
            out_class = da.where(da.isfinite(out_class), out_class, 0)

        # Reshape when writing out
        out_class = out_class.reshape(len(y), len(x))

        # stack back into xarray
        output_xr = xr.DataArray(out_class, coords={"x": x, "y": y}, dims=["y", "x"])

        output_xr = output_xr.to_dataset(name="predictions")

        if proba is True:
            print("   probabilities...")
            out_proba = model.predict_proba(input_data_flattened)

            # convert to %
            out_proba = da.max(out_proba, axis=1) * 100.0

            if clean is True:
                out_proba = da.where(da.isfinite(out_proba), out_proba, 0)

            out_proba = out_proba.reshape(len(y), len(x))

            out_proba = xr.DataArray(
                out_proba, coords={"x": x, "y": y}, dims=["y", "x"]
            )
            output_xr["probabilities"] = out_proba

        return assign_crs(output_xr, str(crs))

    if dask is True:
        # convert model to dask predict
        model = ParallelPostFit(model)
        with joblib.parallel_backend("dask"):
            output_xr = _predict_func(model, input_xr, persist, proba, clean)

    else:
        output_xr = _predict_func(model, input_xr, persist, proba, clean).compute()

    return output_xr
