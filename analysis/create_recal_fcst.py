import glob

import numpy as np
import xarray as xr
from scores.processing import broadcast_and_match_nan
from sklearn.isotonic import IsotonicRegression
from tqdm import tqdm


HRRR_PATH27 = "../data/neighbourhood/hrrr_21_27/"
HRRR_PATH9 = "../data/neighbourhood/hrrr_7_9/"
HRRR_PATH1 = "../data/neighbourhood/hrrr_1_1/"
GRAPH_PATH = "../data/neighbourhood/graphcast_1/"
GRAPH_PATH3 = "../data/neighbourhood/graphcast_3/"
OBS_DATA_PATH = "../data/processed/obs/"

RESULTS_PATH = "../data/recal/"


def recalibrate_fcst(fcst, obs, filename):
    fcst, obs = broadcast_and_match_nan(fcst, obs)

    fcst_recalibrated = xr.full_like(fcst, np.nan)
    iso_reg = IsotonicRegression()

    for station in tqdm(fcst.station.values, desc="Stations"):
        for lead in fcst.lead_time.values:
            for member in fcst.ens_mem.values:
                x = fcst.sel(station=station, lead_time=lead, ens_mem=member).values
                y = obs.sel(station=station, lead_time=lead, ens_mem=member).values
                mask = np.isfinite(y) & np.isfinite(x)
                if x[mask].sum() < 1 or y[mask].sum() < 1:
                    # print(f"skipping station {station}")
                    continue
                iso_reg.fit(x[mask], y[mask])
                x_new = x.copy()
                mask_new = ~np.isnan(x)
                x_recal = np.full_like(x_new, np.nan, dtype=np.float64)
                x_recal[mask_new] = iso_reg.predict(x_new[mask_new])
                fcst_recalibrated.loc[
                    dict(station=station, lead_time=lead, ens_mem=member)
                ] = x_recal

    fcst_recalibrated.to_netcdf(f"{RESULTS_PATH}{filename}.nc")


def main():

    obs = xr.open_dataset(OBS_DATA_PATH)
    obs = obs.rename({"valid(UTC)": "time"})
    obs = obs.precip
    obs_orig = obs.copy()

    graphcast3 = xr.open_mfdataset(f"{GRAPH_PATH3}*.nc")
    graphcast3 = graphcast3.apcp
    graphcast3 = graphcast3.compute() * 1000  # convert to mm
    graphcast3 = graphcast3.clip(min=0)

    def _ensure_time_coord(ds):
        ds = ds.expand_dims("time")
        ds = ds.sel(lead_time=slice(graphcast3.lead_time[0], graphcast3.lead_time[-1]))
        return ds

    files = sorted(glob.glob(f"{HRRR_PATH27}hrrr_*.nc"))
    hrrr27 = xr.open_mfdataset(files, preprocess=_ensure_time_coord)
    hrrr27 = hrrr27["APCP_6hr_acc_fcst"]
    hrrr27 = hrrr27.compute()
    recalibrate_fcst(hrrr27, obs_orig, "hrrr21_27")


if __name__ == "__main__":
    main()
