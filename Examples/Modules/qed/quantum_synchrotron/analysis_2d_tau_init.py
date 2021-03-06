#! /usr/bin/env python

# Copyright 2019 Luca Fedeli, Maxence Thevenet
#
# This file is part of WarpX.
#
# License: BSD-3-Clause-LBNL

import yt
import numpy as np
import scipy.stats as st
import sys
sys.path.insert(1, '../../../../warpx/Regression/Checksum/')
import checksumAPI

# This script checks if electrons and positrons initialized with
# Quantum Synchrotron process enabled
# do actually have an exponentially distributed optical depth

# Tolerance
tolerance_rel = 1e-2
print("tolerance_rel: " + str(tolerance_rel))

def check():
    filename = sys.argv[1]
    data_set = yt.load(filename)

    all_data = data_set.all_data()
    res_ele_tau = all_data["electrons", 'particle_optical_depth_QSR']
    res_pos_tau = all_data["positrons", 'particle_optical_depth_QSR']

    loc_ele, scale_ele = st.expon.fit(res_ele_tau)
    loc_pos, scale_pos = st.expon.fit(res_pos_tau)

    # loc should be very close to 0, scale should be very close to 1
    error_rel = np.abs(loc_ele - 0)
    print("error_rel loc_ele: " + str(error_rel))
    assert( error_rel < tolerance_rel )

    error_rel = np.abs(loc_pos - 0)
    print("error_rel loc_pos: " + str(error_rel))
    assert( error_rel < tolerance_rel )

    error_rel = np.abs(scale_ele - 1)
    print("error_rel scale_ele: " + str(error_rel))
    assert( error_rel < tolerance_rel )

    error_rel = np.abs(scale_pos - 1)
    print("error_rel scale_pos: " + str(error_rel))
    assert( error_rel < tolerance_rel )

    test_name = filename[:-9] # Could also be os.path.split(os.getcwd())[1]
    checksumAPI.evaluate_checksum(test_name, filename)

def main():
    check()

if __name__ == "__main__":
    main()

