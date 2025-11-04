import xarray as xr
from scores.probability import tail_tw_crps_for_ensemble

RECAL_PATH = "../data/recal/"

HRRR_PATH21_27 = f"{RECAL_PATH}hrrr21_27.nc"
HRRR_PATH7_9 = f"{RECAL_PATH}hrrr7_9.nc"
HRRR_PATH1 = f"{RECAL_PATH}hrrr1.nc"
GRAPH_PATH = f"{RECAL_PATH}graphcast.nc"
GRAPH_PATH3 = f"{RECAL_PATH}graphcast3.nc"
OBS_DATA_PATH = "../data/processed/obs/"

RESULTS_PATH = "../results/potential"


def main():
    thresholds = xr.open_dataarray("../data/thresholds/grid/clim_0.99.nc")

    obs = xr.open_dataset(OBS_DATA_PATH, chunks="auto")
    obs = obs.rename({"valid(UTC)": "time"})
    obs = obs.precip

    graphcast = xr.open_dataarray(GRAPH_PATH, chunks="auto")
    graphcast = graphcast.clip(min=0)

    graphcast3 = xr.open_dataarray(GRAPH_PATH3, chunks="auto")
    graphcast3 = graphcast3.clip(min=0)

    hrrr1 = xr.open_dataarray(HRRR_PATH1, chunks="auto")
    hrrr7_9 = xr.open_dataarray(HRRR_PATH7_9, chunks="auto")
    hrrr21_27 = xr.open_dataarray(HRRR_PATH21_27, chunks="auto")

    # twCRPS results
    hrrr1_thresholds = thresholds.sel(
        station=thresholds["station"].isin(hrrr1["station"])
    )
    hrrr7_9_thresholds = thresholds.sel(
        station=thresholds["station"].isin(hrrr7_9["station"])
    )
    hrrr21_27_thresholds = thresholds.sel(
        station=thresholds["station"].isin(hrrr21_27["station"])
    )
    graphcast_thresholds = thresholds.sel(
        station=thresholds["station"].isin(graphcast["station"])
    )
    graphcast3_thresholds = thresholds.sel(
        station=thresholds["station"].isin(graphcast3["station"])
    )

    graphcast_p_twcrps_results = tail_tw_crps_for_ensemble(
        graphcast,
        obs,
        "ens_mem",
        threshold=graphcast_thresholds,
        tail="upper",
        preserve_dims=["lead_time", "time", "station"],
    )
    graphcast_p_twcrps_results.to_netcdf(
        f"{RESULTS_PATH}/graphcast_potential_twcrps.nc"
    )

    graphcast3_p_twcrps_results = tail_tw_crps_for_ensemble(
        graphcast3,
        obs,
        "ens_mem",
        method="fair",
        threshold=graphcast3_thresholds,
        tail="upper",
        preserve_dims=["lead_time", "time", "station"],
    )
    graphcast3_p_twcrps_results.to_netcdf(
        f"{RESULTS_PATH}/graphcast3_potential_twcrps.nc"
    )

    hrrr1_p_twcrps_results = tail_tw_crps_for_ensemble(
        hrrr1,
        obs,
        "ens_mem",
        threshold=hrrr1_thresholds,
        tail="upper",
        preserve_dims=["lead_time", "time", "station"],
    )
    hrrr1_p_twcrps_results.to_netcdf(f"{RESULTS_PATH}/hrrr1_potential_twcrps.nc")

    hrrr7_9_p_twcrps_results = tail_tw_crps_for_ensemble(
        hrrr7_9,
        obs,
        "ens_mem",
        method="fair",
        threshold=hrrr7_9_thresholds,
        tail="upper",
        preserve_dims=["lead_time", "time", "station"],
    )
    hrrr7_9_p_twcrps_results.to_netcdf(f"{RESULTS_PATH}/hrrr7_9_potential_twcrps.nc")

    hrrr21_27_p_twcrps_results = tail_tw_crps_for_ensemble(
        hrrr21_27,
        obs,
        "ens_mem",
        method="fair",
        threshold=hrrr21_27_thresholds,
        tail="upper",
        preserve_dims=["lead_time", "time", "station"],
    )
    hrrr21_27_p_twcrps_results.to_netcdf(
        f"{RESULTS_PATH}/hrrr21_27_potential_twcrps.nc"
    )


if __name__ == "__main__":
    main()
