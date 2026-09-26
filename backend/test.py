import importlib.util

try:
    import h5py
except ImportError as e:
    raise RuntimeError(
        "The 'h5py' package is not installed. Please install it with: pip install h5py"
    ) from e

f = h5py.File(
    "../dataset/3RIMG_01APR2024_0545_L1C_SGP_V01R00_B346.h5",
    "r",
)

print(type(f["Projection_Information"]))

print("\nProjection Information:")

proj = f["Projection_Information"]

for key in proj.attrs:
    print(key, ":", proj.attrs[key])