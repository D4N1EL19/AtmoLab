import xarray as xr


direccion = ("data/M2T1NXSLV.5.12.4%3AMERRA2_300.tavg1_2d_slv_Nx.20100601.nc4.dap-2.nc4")

dataset = xr.open_dataset(direccion)

datos_bc = dataset[["T2M", "QV2M", "U2M", "V2M"]].sel(
    lat=31,
    lon=-116,
    method="nearest"
)
dataframe = datos_bc.to_dataframe()
df_final = dataframe.reset_index()
df_final.to_csv('datos_climaticos_filtrados.csv', index=True)
print(datos_bc)