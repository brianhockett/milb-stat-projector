import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup

def plot_slashline(milb : pd.DataFrame, y0 : pd.DataFrame, y1 : pd.DataFrame, y2 : pd.DataFrame, ax :plt.Axes):
    
    milb_avg, milb_obp, milb_slg, milb_woba = milb['BA'], milb['OBP'], milb['SLG'], milb['wOBA']
    y0_avg, y0_obp, y0_slg, y0_woba = y0['BA_0'], y0['OBP_0'], y0['SLG_0'], y0['wOBA_0']
    y1_avg, y1_obp, y1_slg, y1_woba = y1['BA_1'], y1['OBP_1'], y1['SLG_1'], y1['wOBA_1']
    y2_avg, y2_obp, y2_slg, y2_woba = y2['BA_2'], y2['OBP_2'], y2['SLG_2'], y2['wOBA_2']
    avg = np.array([y0_avg, y1_avg, y2_avg])
    obp = np.array([y0_obp, y1_obp, y2_obp])
    slg = np.array([y0_slg, y1_slg, y2_slg])
    woba = np.array([y0_woba, y1_woba, y2_woba])
    years = [0, 1, 2]
    name = milb['Player'].iloc[0]
    last_name, first_name = name.split(", ")

    colors = {
        'AVG': '#4C9EE7',      # Light Blue
        'OBP': '#FF7F7F',      # Salmon Pink
        'SLG': '#2E8B57',      # Forest Green
        'wOBA': '#9B59B6',     # Purple
    }

    # Plot MLB Projection
    ax.plot(years, avg, linestyle='--', marker='o', color=colors['AVG'], label='MLB AVG')
    ax.plot(years, obp, linestyle='--', marker='o', color=colors['OBP'], label='MLB OBP')
    ax.plot(years, slg, linestyle='--', marker='o', color=colors['SLG'], label='MLB SLG')
    ax.plot(years, woba, linestyle='--', marker='o', color=colors['wOBA'], label='MLB wOBA')

    # Plot MiLB stats
    ax.plot(years, 3 * [milb_avg], linestyle='-', linewidth = 0.5, alpha = 0.5, color=colors['AVG'], label='MiLB AVG')
    ax.plot(years, 3 * [milb_obp], linestyle='-', linewidth = 0.5, alpha = 0.5, color=colors['OBP'], label='MiLB OBP')
    ax.plot(years, 3 * [milb_slg], linestyle='-', linewidth = 0.5, alpha = 0.5, color=colors['SLG'], label='MiLB SLG')
    ax.plot(years, 3 * [milb_woba], linestyle='-', linewidth = 0.5, alpha = 0.5, color=colors['wOBA'], label='MiLB wOBA') 
    ax.set_xticks(years)
    ax.set_ylim(avg.min() - 0.1, slg.max() + 0.1)
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    ax.set_title(f'MLB Slashline Projection for {first_name + " " + last_name}')
    ax.set_xlabel('Years Since Debut')

    for i in range(len(years)):
        ax.text(years[i], float(avg[i]) + 0.02, f'{float(avg[i]):.3f}', ha='center', color='black')
        ax.text(years[i], float(obp[i]) + 0.02, f'{float(obp[i]):.3f}', ha='center', color='black')
        ax.text(years[i], float(slg[i]) + 0.02, f'{float(slg[i]):.3f}', ha='center', color='black')
        ax.text(years[i], float(woba[i]) + 0.02, f'{float(woba[i]):.3f}', ha='center', color='black')

def plot_k_and_bb(milb : pd.DataFrame, y0 : pd.DataFrame, y1 : pd.DataFrame, y2 : pd.DataFrame, ax :plt.Axes):
    milb_k, milb_bb, milb_k_min_bb = milb['K%'], milb['BB%'], milb['K%'] - milb['BB%']
    y0_k, y0_bb, y0_k_min_bb = y0['K%_0'], y0['BB%_0'], y0['K%_0'] - y0['BB%_0']
    y1_k, y1_bb, y1_k_min_bb = y1['K%_1'], y1['BB%_1'], y1['K%_1'] - y1['BB%_1']
    y2_k, y2_bb, y2_k_min_bb = y2['K%_2'], y2['BB%_2'], y2['K%_2'] - y2['BB%_2']

    k = np.round(np.array([y0_k, y1_k, y2_k]), 1)
    bb = np.round(np.array([y0_bb, y1_bb, y2_bb]), 1)
    k_min_bb = np.round(np.array([y0_k_min_bb, y1_k_min_bb, y2_k_min_bb]), 1)

    name = milb['Player'].iloc[0]
    last_name, first_name = name.split(", ")

    colors = {
        'K%': '#4C9EE7',      # Light Blue
        'BB%': '#2E8B57',      # Forest Green
        'K%-BB%': '#9B59B6',     # Purple
    }

    years = [0, 1, 2]
    
    # Plot MLB Projection
    ax.plot(years, k, label = 'MLB K%', color = colors['K%'], linestyle='--', marker='o')
    ax.plot(years, bb, label = 'MLB BB%', color = colors['BB%'], linestyle='--', marker='o')
    ax.plot(years, k_min_bb, label = 'MLB K%-BB%', color = colors['K%-BB%'], linestyle='--', marker='o')

    # Plot MiLB Stats
    ax.plot(years, 3 * [milb_k], label = 'MiLB K%', color = colors['K%'], linestyle = '-', linewidth = 0.5, alpha = 0.5)
    ax.plot(years, 3 * [milb_bb], label = 'MiLB BB%', color = colors['BB%'], linestyle = '-', linewidth = 0.5, alpha = 0.5)
    ax.plot(years, 3 * [milb_k_min_bb], label = 'MiLB K%-BB%', color = colors['K%-BB%'], linestyle = '-', linewidth = 0.5, alpha = 0.5)

    ax.set_xticks(years)
    ax.set_ylim(max(min(bb.min(), k.min(), k_min_bb.min()) - 4, 0), max(bb.max(), k.max(), k_min_bb.max()) + 4)
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    ax.set_title(f'MLB Strikeout and Walk Projections for {first_name + " " + last_name}')
    ax.set_xlabel('Years Since Debut')

    for i in range(len(years)):
        ax.text(years[i], float(k[i]) + 0.02, f'{float(k[i]):.1f}', ha='center', color='black')
        ax.text(years[i], float(bb[i]) + 0.02, f'{float(bb[i]):.1f}', ha='center', color='black')
        ax.text(years[i], float(k_min_bb[i]) + 0.02, f'{float(k_min_bb[i]):.1f}', ha='center', color='black')
