# script for pySPEDAS tutorial at the 2019 Winter Community Workshop
# agenda:
# 1. installation; requirements
# 2. loading MMS data
# 3. plotting MMS data
# 4. working with the data vales, timestamps and metadata
# 5. analysis tools

###############################################################

# 2. loading MMS data

from pyspedas.mms import mms_load_fgm, mms_load_eis

mms_load_fgm(trange=['2015-10-16', '2015-10-17'])

# the load routines accept all of the standard keywords
mms_load_eis(probe='4', data_rate='brst', datatype=['extof', 'phxtof'], trange=['2015-10-16/13:05', '2015-10-16/13:10'])

# list the current tplot variables

from pytplot import tplot_names

tplot_names()

from pyspedas.mms import mms_load_fpi, mms_load_eis

###############################################################
# 3. plotting MMS data

from pytplot import tplot

tplot('mms1_fgm_b_gsm_srvy_l2')

tplot(['mms4_epd_eis_brst_phxtof_proton_flux_omni', 'mms4_epd_eis_brst_extof_proton_flux_omni'])

from pyspedas.mms import mms_load_fpi

mms_load_fpi(probe='4', data_rate='brst', datatype='des-moms', trange=['2015-10-16/13:00', '2015-10-16/13:10'])

tplot(['mms4_des_energyspectr_omni_brst', 'mms4_des_pitchangdist_miden_brst', 'mms4_des_bulkv_gse_brst', 'mms4_des_numberdensity_brst'])


###############################################################
# 4. working with the data vales, timestamps and metadata

from pytplot import get_data, store_data

# extract the data from a tplot variable
times, data = get_data('mms1_fgm_b_gsm_srvy_l2')

# e.g.,
# >>> times[0]
# 1444953613.330852
# >>> data[0]
# array([ 8580.49 ,  7339.21 ,  6250.034, 12905.493], dtype=float32)

# convert the unix time to a string

from pyspedas.utilities.time_string import time_string

print(time_string(1444953613.330852))

from pyspedas.utilities.time_double import time_double

print(time_double('2015-10-16 00:00:13.330852'))

# create new tplot variables

store_data('b_gsm_vec', data={'x': times, 'y': data[:,0:3]}) # B-field vector

store_data('b_gsm_mag', data={'x': times, 'y': data[:,3]}) # B-field magnitude

tplot(['b_gsm_mag', 'b_gsm_vec'])

# modify variable metadata

from pytplot import options

options('b_gsm_mag', 'ytitle', 'B-field magnitude')
options('b_gsm_vec', 'ytitle', 'B-field vector')
options('b_gsm_vec', 'color', ['b', 'g', 'r'])
options('b_gsm_vec', 'legend_names', ['Bx', 'By', 'Bz'])

tplot(['b_gsm_mag', 'b_gsm_vec'])

# save the data to ASCII files
from pyspedas.utilities.tplot2ascii import tplot2ascii
tplot2ascii(['b_gsm_mag', 'b_gsm_vec'])

###############################################################
# 5. analysis tools

# clip to a certain time
from pyspedas.analysis.time_clip import time_clip

time_clip('b_gsm_vec', '2015-10-16/10:00', '2015-10-16/14:00')

options('b_gsm_vec-tclip', 'color', ['r', 'g', 'b'])
options('b_gsm_vec', 'legend_names', ['Bx', 'By', 'Bz'])
tplot('b_gsm_vec-tclip')

# clip the data
from pyspedas.analysis.tclip import tclip

tclip('b_gsm_vec-tclip', -20, 20)

# subtract the average
from pyspedas.analysis.subtract_average import subtract_average

subtract_average('mms1_fgm_b_gsm_srvy_l2')

tplot('mms1_fgm_b_gsm_srvy_l2-d')

