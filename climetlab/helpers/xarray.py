# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import numpy as np


class XArrayHelper:
    def __init__(self, data):

        # data.climetlab.foo(42)

        self.data = data
        for name, var in data.data_vars.items():
            self.name = name
            self.var = var
            self.extra_dims = var.dims[:-2]
            break

        lat, lon = self.var.dims[-2], self.var.dims[-1]

        data[lat].attrs["standard_name"] = "latitude"
        data[lon].attrs["standard_name"] = "longitude"

        self.north = np.amax(data[lat].data)
        self.south = np.amin(data[lat].data)
        self.east = np.amax(data[lon].data)
        self.west = np.amin(data[lon].data)

    def plot_map(self, driver):
        driver.bounding_box(
            north=self.north, south=self.south, west=self.west, east=self.east
        )

        dimension_settings = dict()

        for d in self.extra_dims:
            dimension_settings[d] = 0  # self.data[d].data[0]

        driver.plot_xarray(self.data, self.name, dimension_settings)


def helper(data, *args, **kwargs):
    import xarray as xr

    if isinstance(data, xr.Dataset):
        return XArrayHelper(data, *args, **kwargs)

    return XArrayHelper(data.to_dataset(), *args, **kwargs)
