# threshold-weighted-spatial-code

Order to run code:
1. Run notebooks to download data in `./download_data`. This will not only download the data, but also do a small amount of preprocessing.
2. Run notebooks in `./data_preprocessing`. These will do some data wrangling to get organise the data.
3. Run notebooks in `./produce_neighbourhoods`. These will generate the the "psuedo-ensembles" based on the various neighbourhood sizes. The `create_hrrr_ens_xy_neighborhood.ipynb` notebook needs to be run three times, once for each neighbourhood size for the HRRR
4. Run the `./clim/generate_grid_clim.ipynb` followed by `./clim/generate_point_clim.ipynb` notebooks to generate the climatological thresholds.
5. Run the `./weights/density weights.ipynb` notebook to generate the station density weights.
5. Run the notebooks in `./analysis`.
6. Run the scripts `create_recal_fcst.py`, then `dsc_score.py` in `./analysis`.
7. Before generating the figures, run `generate_figures/prep_data_for_twcrps_by_lead_time.ipynb`.
8. Run the the other notebooks in `generate_figures` to produce the figures for the paper.

