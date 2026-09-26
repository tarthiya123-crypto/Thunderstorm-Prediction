import h5py

f = h5py.File(
    "../dataset/3RIMG_01APR2024_0545_L1C_SGP_V01R00_B346.h5",
    "r"
)

proj = f["Projection_Information"]

for key in proj.attrs:
    print(key, ":", proj.attrs[key])