import data_loader
import name_dic
import numpy as np
from data_processor import (
    process_trendy_nbp,
    process_trendy_ra,
    process_trendy_rh,
    process_trendy_gpp,
    process_trendy_fLuc,
    process_trendy_fFire,
    process_trendy_lai,
    ProcessTM5GOSAT,
    ProcessTRENDY,
    ProcessTM5IS,
    ProcessFire,
    ProcessFluxcom,
    ProcessFluxcomX,
    ProcessTM5Prior,
    ProcessLai,
    ProcessSIF,
    ProcessERA5,
    ProcessOCO,
    ProcessOCO2MIP,
    ProcessSIFbaseGPP,
    ProcessNIRvGPP,
    ProcessAll
)
import read_pkl
import matplotlib.gridspec as gridspec
from statistical_analysis import change_order
from statistical_analysis import colum_filter
from settings import order
from read_pkl import data
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
import matplotlib.pyplot as plt
from plots import plots_design
def make_GPP_NIRv_dictionary(group_list, time_type, time):
    keys         = np.append(group_list, ['NIRv', 'time'])
    GPP          = dict.fromkeys(keys, None)
    GPP['time']  = time
    if time_type == 'monthly':
        GPP['NIRv'] = data.est['nirvgpp'].timeseries['GPP']
        for model in group_list:
            GPP[model] = data.trendy['gpp'].timeseries[model]
    if time_type == 'season':
        GPP['NIRv'] = change_order(data.est['nirvgpp'].season_cyc['GPP'], order)
        GPP['NIRv'] = colum_filter(GPP['NIRv'], 'index')
        for model in group_list:
            GPP[model] = change_order(data.trendy['gpp'].season_cyc[model], order)
            GPP[model] = colum_filter(GPP[model], 'index')
    return GPP
def plt_nirv_gpp(ax, group_list, value):
    #nirv_time = data_loader.create_date('2009-01-01', '2017-12-31')['range']
    ax = VisualLines(ax, value['time']).nirv_gpp(value['NIRv']).ax
    for model in group_list:
        ax.plot(value['time'], value[model],label=model, linewidth=1)
    return ax
class CompareGPPNIRv:
    def __init__(self, ax, group_list):
        self.ax         = ax
        self.group_list = group_list
    def monthly(self, time):
        gpps    = make_GPP_NIRv_dictionary(self.group_list, 'monthly', time)
        self.ax = MonthlyPlot(self.ax).co2_flux().ax
        nirv_time = data_loader.create_date('2009-01-01', '2017-12-31')['range']
        self.ax = VisualLines(self.ax, nirv_time).nirv_gpp(gpps['NIRv']).ax
        for model in self.group_list:
            self.ax.plot(gpps['time'], gpps[model], label=model, linewidth=1)
        return self
    def season(self, time):
        gpps    = make_GPP_NIRv_dictionary(self.group_list, 'season', time)
        self.ax = SeasonPlot(self.ax).co2_flux().ax
        self.ax = plt_nirv_gpp(self.ax, self.group_list, gpps)
        self.ax.set_xticks([3, 6, 9, 12])
        return self
def plt_mn_season(name_lists):
    plot_mon, plot_sea = plots_design.mn_season().ini_fig()
    plot_mon = CompareGPPNIRv(plot_mon, name_lists).monthly(time).ax
    plot_sea = CompareGPPNIRv(plot_sea, name_lists).season(month).ax

    plots_design.mn_season().same_ylim(plot_mon, plot_sea)
    plots_design.mn_season().optimiz_fig(plot_mon, plot_sea)
    plt.show()
print(__name__)
if __name__.split('.')[-1] == 'plot_NIRvGPP':
    from settings import trendy_models as models
    time  = data.trendy['gpp'].dates['range']
    month = np.arange(1, 13, 1, dtype='int')
    good  = data.trendy['nbp'].good_name
    ok    = data.trendy['nbp'].ok_name
    bad   = data.trendy['nbp'].bad_name
    """
    plt_mn_season(good)
    plt_mn_season(ok)
    plt_mn_season(bad)
    """
    plt_mn_season(models)