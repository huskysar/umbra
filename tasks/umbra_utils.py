import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Our quota is constrained to certain combinations of rangeResolutionMinMeters and multilookFactor
# for which there are recommended grazingAngle ranges
# https://docs.canopy.umbra.space/docs/suggested-tasking-parameters

# Pick one of these: 
# $675
acquisition_1_1 = {
    "rangeResolutionMinMeters": 1,
    "multilookFactor": 1,
    "grazingAngleMinDegrees": 42,
    "grazingAngleMaxDegrees": 80,
}

# $850
acquisition_1_2 = {
    "rangeResolutionMinMeters": 1,
    "multilookFactor": 2,
    "grazingAngleMinDegrees": 37,
    "grazingAngleMaxDegrees": 80,
}

# $1,200
acquisition_1_4= {
    "rangeResolutionMinMeters": 1,
    "multilookFactor": 4,
    "grazingAngleMinDegrees": 32,
    "grazingAngleMaxDegrees": 80,
}

# $3,250
acquisition_025_1= {
    "rangeResolutionMinMeters": 0.25,
    "multilookFactor": 1,
    "grazingAngleMinDegrees": 53,
    "grazingAngleMaxDegrees": 59,
}

def plot_feasibilities_polar(df, incidence_range='auto', satnames=False):
    ''' incidence_range = None (auto) 'full' or 'squeeze' '''
    # Quick plot of acquisition geometries 
    theta = np.deg2rad(df['targetAzimuthAngle'])
    radii = 90-df['grazingAngle'] #incidence angle
    width = np.deg2rad(df['targetAzimuthAngleEndDegrees'] - df['targetAzimuthAngleStartDegrees'])
    
    # colors = df.squintAngleEngineering
    # colors /= np.max(np.abs(colors),axis=0) 
    # colors = plt.cm.bwr(colors) 
    # colors = plt.cm.Spectral_r(colors)
    colors = None

    # Clockwise, north=0, r_origin = min incidence
    ax = plt.subplot(projection='polar')
    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)

    # Getting bars on polar plot is fussy it turns out...
    bottom=None
    height=radii
    if incidence_range == 'full':
        ax.set_rlim(10,80) # pad 20-70 whitch is the stated full range in umbra docs
    if incidence_range == 'auto':
        pad = 1 # degree (incidence)
        rmin = int(radii.min())
        origin = rmin-pad
        ax.set_rorigin(origin)
        bottom = rmin
        height = radii - rmin
        ax.set_rlim(rmin, radii.max()+pad) # stated full range in docs
    # NOTE: bar charts only work correctly when rorigin=-ylim
    # https://stackoverflow.com/questions/40836983/bars-on-polar-bar-plots-are-cut-off-when-rlim-is-set
    # Really want a 'broken' floating radial axis that starts at 20 but is linear
    ax.bar(x=theta, height=height, bottom=bottom,  width=width, color=colors, alpha=0.2) #add colorbar?
    ax.bar(x=theta, height=height, bottom=bottom, width=np.deg2rad(0.5), color='k')

    # Add centerpoints labeled by satellite
    if satnames:
        for name,group in df.groupby('satelliteId'):
            theta = np.deg2rad(group['targetAzimuthAngle'])
            radii = 90-group['grazingAngle']
            ax.scatter(theta, radii, label=name)
        # https://matplotlib.org/stable/gallery/pie_and_polar_charts/polar_legend.html
        # NOTE: ax legend anchor is 0:1 axes coords
        ax.legend(loc="center", bbox_to_anchor=(0.5, 0.15))
    # Add previous acquisition
    # ax.scatter(np.deg2rad(gf['view:azimuth']), 
    #         90-gf['umbra:grazing_angle_degrees'], 
    #         #color='r', 
    #         s=100)
    # ax.text(np.deg2rad(gf['view:azimuth'].iloc[0]), 
    #         90-gf['umbra:grazing_angle_degrees'].iloc[0], 
    #         #gf['umbra:task_id'].iloc[0]
    #         gf['datetime'].iloc[0][:10]
    # )

    label_position=ax.get_rlabel_position()
    offset = np.diff(ax.get_yticks())[0]
    ax.text(np.radians(label_position), ax.get_rmax()+offset,
            'view:incidence',
            rotation=None, ha='center',va='bottom')

    ax.set_xlabel('view:azimuth')

    titlestr = f'{len(df)} Feasible Acquisitions\n{df['windowStartAt'].min().rstrip('+00:00')} to {df['windowEndAt'].max().rstrip('+00:00')}'
    plt.title(titlestr)

    return ax


def plot_feasibilities_squint(df):
    ''' incidence_range = None (auto) 'full' or 'squeeze' '''
    viz = df.sort_values(by='satelliteId')
    viz['windowStartAt'] = pd.to_datetime(viz['windowStartAt'])

    fig, ax = plt.subplots(figsize=(12,4))
    markers = ['o', '^', 'd', 's']
    for name,group in viz.groupby('satelliteId'):
        plt.scatter(x=group['windowStartAt'], y=group['targetAzimuthAngle'], c=group['squintAngleEngineering'],
                    marker=markers.pop(),
                    s=100,
                    alpha=0.8,
                    label=name,
                    vmin=-90,
                    vmax=90,
                    cmap='bwr', ec='k')

    cb = plt.colorbar();
    cb.set_label('squintAngleEngineering')

    plt.ylabel('view:azimuth')
    plt.axhline(180, color='k', linestyle='--', linewidth=0.5)
    plt.axhline(90, color='k', linestyle='--', linewidth=0.5)
    plt.axhline(270, color='k', linestyle='--', linewidth=0.5)
    plt.legend()
    titlestr = f'{len(df)} Feasible Acquisitions\n{df['windowStartAt'].min().rstrip('+00:00')} to {df['windowEndAt'].max().rstrip('+00:00')}'
    plt.title(titlestr);

    return ax


def plot_feasibilities_incidence(df):
    ''' incidence_range = None (auto) 'full' or 'squeeze' '''
    viz = df.sort_values(by='satelliteId')
    viz['windowStartAt'] = pd.to_datetime(viz['windowStartAt'])

    fig, ax = plt.subplots(figsize=(12,4))
    #plt.scatter(x=viz['windowStartAt'], y=viz['targetAzimuthAngle'], s=100, alpha=0.8, c=viz['incidenceAngle'],cmap='viridis', ec='k')
    markers = ['o', '^', 'd', 's']
    for name,group in viz.groupby('satelliteId'):
        plt.scatter(x=group['windowStartAt'], y=group['targetAzimuthAngle'], c=group['incidenceAngle'],
                    marker=markers.pop(),
                    s=100,
                    alpha=0.8,
                    label=name,
                    cmap='viridis', ec='k')

    cb = plt.colorbar();
    cb.set_label('view:incidence')

    plt.ylabel('view:azimuth')
    plt.axhline(180, color='k', linestyle='--', linewidth=0.5)
    plt.axhline(90, color='k', linestyle='--', linewidth=0.5)
    plt.axhline(270, color='k', linestyle='--', linewidth=0.5)
    titlestr = f'{len(df)} Feasible Acquisitions\n{df['windowStartAt'].min().rstrip('+00:00')} to {df['windowEndAt'].max().rstrip('+00:00')}'
    plt.title(titlestr)
    plt.legend()

    return ax