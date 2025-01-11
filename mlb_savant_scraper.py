import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

years = [i for i in range(2021, 2025)]

home_dir = os.path.dirname(__file__)
data_dir = os.path.join(home_dir, 'mlb_data')

# Scraping Batter Data
for year in years:
    print(f"Scraping MLB Batter Data for {year}\n")
    batter_url = f'https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea={year}%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInn=&hfBBT=&hfFlag=is%5C.%5C.tracked%7C&hfLevel=&metric_1=&hfTeamAffiliate=&hfOpponentAffiliate=&group_by=name&min_pitches=0&min_results=150&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&chk_stats_pa=on&chk_stats_abs=on&chk_stats_bip=on&chk_stats_hits=on&chk_stats_singles=on&chk_stats_dbls=on&chk_stats_triples=on&chk_stats_hrs=on&chk_stats_so=on&chk_stats_k_percent=on&chk_stats_bb=on&chk_stats_bb_percent=on&chk_stats_whiffs=on&chk_stats_swings=on&chk_stats_ba=on&chk_stats_xba=on&chk_stats_obp=on&chk_stats_xobp=on&chk_stats_slg=on&chk_stats_xslg=on&chk_stats_woba=on&chk_stats_xwoba=on&chk_stats_barrels_total=on&chk_stats_babip=on&chk_stats_iso=on&chk_stats_swing_miss_percent=on&chk_stats_launch_speed=on&chk_stats_hyper_speed=on&chk_stats_launch_angle=on&chk_stats_bbdist=on&chk_stats_hardhit_percent=on&chk_stats_barrels_per_bbe_percent=on&chk_stats_barrels_per_pa_percent=on&chk_is..tracked=on#result'
    
    response = requests.get(batter_url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {year}")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')
    table_html = soup.find('table')

    data = []
    if table_html:
        headers = [th.text.strip() for th in table_html.find('thead').find_all('th') if th.text.strip()]
        headers = headers[1:]
        rows = table_html.find('tbody').find_all('tr')

        for row in rows:
            stats = [td.text.strip().replace("\n", "") for td in row.find_all('td') if td.parent.get('class') != ['expand-child']]
            if stats:
                stats = stats[2:]
                stats = stats[:-1]
                data.append(stats)
    
    if data:
        df = pd.DataFrame(data, columns = headers)
        filename = os.path.join(data_dir, f'mlb_batter_{year}.csv')
        df.to_csv(filename, index = False)
        print(f'MLB Batter Data for {year} Saved to {filename}\n')
    else:
        print(f'No MLB Batter Data for {year}\n')    

    time.sleep(1)

# Scraping Pitcher Data
for year in years:
    print(f"Scraping MLB Pitcher Data for {year}\n")
    pitcher_url = f'https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea={year}%7C&hfSit=&player_type=pitcher&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInn=&hfBBT=&hfFlag=is%5C.%5C.tracked%7C&hfLevel=&metric_1=&hfTeamAffiliate=&hfOpponentAffiliate=&group_by=name&min_pitches=0&min_results=150&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&chk_stats_pa=on&chk_stats_abs=on&chk_stats_bip=on&chk_stats_hits=on&chk_stats_singles=on&chk_stats_dbls=on&chk_stats_triples=on&chk_stats_hrs=on&chk_stats_so=on&chk_stats_k_percent=on&chk_stats_bb=on&chk_stats_bb_percent=on&chk_stats_whiffs=on&chk_stats_swings=on&chk_stats_api_break_z_with_gravity=on&chk_stats_api_break_x_arm=on&chk_stats_api_break_z_induced=on&chk_stats_api_break_x_batter_in=on&chk_stats_ba=on&chk_stats_xba=on&chk_stats_obp=on&chk_stats_xobp=on&chk_stats_slg=on&chk_stats_xslg=on&chk_stats_woba=on&chk_stats_xwoba=on&chk_stats_barrels_total=on&chk_stats_babip=on&chk_stats_iso=on&chk_stats_swing_miss_percent=on&chk_stats_velocity=on&chk_stats_effective_speed=on&chk_stats_spin_rate=on&chk_stats_release_pos_z=on&chk_stats_release_pos_x=on&chk_stats_release_extension=on&chk_stats_plate_x=on&chk_stats_plate_z=on&chk_stats_launch_speed=on&chk_stats_hyper_speed=on&chk_stats_launch_angle=on&chk_stats_bbdist=on&chk_stats_hardhit_percent=on&chk_stats_barrels_per_bbe_percent=on&chk_stats_barrels_per_pa_percent=on&chk_is..tracked=on#results'

    response = requests.get(pitcher_url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {year}")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')
    table_html = soup.find('table')

    data = []
    if table_html:
        headers = [th.text.strip() for th in table_html.find('thead').find_all('th') if th.text.strip()]
        headers = headers[1:]
        rows = table_html.find('tbody').find_all('tr')

        for row in rows:
            stats = [td.text.strip().replace("\n", "") for td in row.find_all('td') if td.parent.get('class') != ['expand-child']]
            if stats:
                stats = stats[2:]
                stats = stats[:-1]
                data.append(stats)
    
    if data:
        df = pd.DataFrame(data, columns = headers)
        filename = os.path.join(data_dir, f'mlb_pitcher_{year}.csv')
        df.to_csv(filename, index = False)
        print(f'MLB Pitcher Data for {year} Saved to {filename}\n')
    else:
        print(f'No MLB Pitcher Data for {year}\n')    

    time.sleep(1)

