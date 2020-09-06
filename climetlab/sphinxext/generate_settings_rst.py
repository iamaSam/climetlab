#!/usr/bin/env python3
# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import os
import getpass

from climetlab.core.settings import SETTINGS_AND_HELP

HOME = os.path.expanduser("~/")
USER = getpass.getuser()


def tidy(x):

    if isinstance(x, (list, tuple)):
        return [tidy(y) for y in x]

    if isinstance(x, dict):
        d = {}
        for k, v in x.items():
            d[k] = tidy(v)
        return d

    if isinstance(x, str):
        if x.startswith(HOME):
            n = len(HOME)
            return tidy("~/{}".format(x[n:]))

        if "-" + USER in x:
            return tidy(x.replace("-" + USER, "-${USER}"))

    return x


def execute():

    print()
    print(".. list-table::")
    print("   :header-rows: 1")
    print("   :widths: 10 10 80")
    print()
    print("   * - | Name")
    print("     - | Default")
    print("     - | Description")
    print()
    for k, v in sorted(tidy(SETTINGS_AND_HELP).items()):
        print("   * - |", k)
        print("     - |", v[0])
        print("     - |", v[1])
    print()


if __name__ == "__main__":
    execute()