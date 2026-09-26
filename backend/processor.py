try:
    import h5py  # pyright: reportMissingImports=false  # type: ignore[import-not-found]
except Exception as e:
    raise ImportError(
        "h5py is required to run processor.py. Install it with: pip install h5py\n"
        f"Original error: {e}"
    )
import numpy as np
import pandas as pd
from scipy import ndimage
from scipy.ndimage import center_of_mass
import os
import re

def process_insat_file(filename):

    f = h5py.File(filename, "r")

    tir1 = f["TIR1_BT"][0]
    tir2 = f["TIR2_BT"][0]
    wv   = f["WV_BT"][0]

    # Cloud mask
    cloud_mask = tir1 < 240

    # Label clouds
    labeled_clouds, num_clouds = ndimage.label(cloud_mask)

    sizes = ndimage.sum(
        cloud_mask,
        labeled_clouds,
        range(1, num_clouds + 1)
    )

    large_cloud_mask = np.zeros_like(cloud_mask)

    for i, size in enumerate(sizes):
        if size > 500:
            large_cloud_mask[labeled_clouds == i + 1] = True

    labeled_large, num_large = ndimage.label(
        large_cloud_mask
    )

    cloud_data = []

    for cloud_id in range(1, num_large + 1):

        mask = (labeled_large == cloud_id)

        area_pixels = mask.sum()

        min_temp = tir1[mask].min()
        mean_temp = tir1[mask].mean()

        y, x = center_of_mass(mask)

        tir2_mean = tir2[mask].mean()
        tir2_min  = tir2[mask].min()

        wv_mean = wv[mask].mean()
        wv_min  = wv[mask].min()

        cloud_data.append([
            cloud_id,
            area_pixels,
            min_temp,
            mean_temp,
            x,
            y,
            tir2_mean,
            tir2_min,
            wv_mean,
            wv_min
        ])

    df = pd.DataFrame(
        cloud_data,
        columns=[
            "CloudID",
            "AreaPixels",
            "MinTemp",
            "MeanTemp",
            "X",
            "Y",
            "TIR2_Mean",
            "TIR2_Min",
            "WV_Mean",
            "WV_Min"
        ]
    )

    df["BTD_TIR1_TIR2"] = (
        df["MeanTemp"] - df["TIR2_Mean"]
    )

    df["BTD_WV_TIR1"] = (
        df["WV_Mean"] - df["MeanTemp"]
    )

    # Extract date/time from filename
    basename = os.path.basename(filename)

    match = re.search(
        r'(\d{2}[A-Z]{3}\d{4})_(\d{4})',
        basename
    )

    if match:
        df["Date"] = match.group(1)
        df["Time"] = match.group(2)

    return df