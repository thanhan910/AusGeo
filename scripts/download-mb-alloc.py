# Download all xlsx files from "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/allocation-files" and save them as CSV files in the "data/mb-allocation" directory.
# These files detail the allocation of Mesh blocks to geographical areas.

import pandas as pd
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time

# root_directory = "AusGeo"
root_directory = ".."
data_directory = f'{root_directory}/data/core/mb-alloc'

os.makedirs(data_directory, exist_ok=True)


# Crawl all xlsx and csv files from website


# URL of the webpage containing links to XLSX and CSV files
url = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/allocation-files"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all links on the webpage
links = soup.find_all("a")

hrefs = [link.get("href") for link in links]
hrefs = [urljoin(url, href) for href in hrefs if href is not None]

xlsx_hrefs = [href for href in hrefs if href.endswith(".xlsx") or href.endswith(".csv")]
xlsx_hrefs = [urljoin(url, href) for href in xlsx_hrefs]

for href in xlsx_hrefs:
    name = href.split("/")[-1].split(".")[0]
    time_0 = time.perf_counter()
    print(f'[{name}]', 'Start downloading...')
    df = pd.read_excel(href, dtype=str)
    time_1 = time.perf_counter()
    print(f'[{name}]', 'Excel downloaded', time_1 - time_0)
    df.to_csv(f'{data_directory}/{name}.csv', index=False)
    time_2 = time.perf_counter()
    print(f'[{name}]', 'Saved to CSV', time_2 - time_1)

# dfs = { href.split("/")[-1].split(".")[0] : pd.read_excel(href) for href in xlsx_hrefs }
# # 30m

# os.makedirs(data_directory, exist_ok=True)

# for name, df in dfs.items():
#   df.to_csv(f'{data_directory}/{name}.csv', index=False)
# # 1m

table_names = {
  'MB_2021_AUST': 'Mesh Blocks - 2021',
  'SA1_2021_AUST': 'Statistical Areas Level 1 - 2021',
  'SA2_2021_AUST': 'Statistical Areas Level 2 - 2021',
  'SA3_2021_AUST': 'Statistical Areas Level 3 - 2021',
  'SA4_2021_AUST': 'Statistical Areas Level 4 - 2021',
  'GCCSA_2021_AUST': 'Greater Capital City Statistical Areas - 2021',
  'STE_2021_AUST': 'States and Territories - 2021',
  'AUS_2021_AUST': 'Australia - 2021',
  'INDIGENOUS_STRUCTURE_ALLOCATION_2021': 'Indigenous Structure - 2021',
  'ILOC_2021_AUST': 'Indigenous Locations - 2021',
  'IARE_2021_AUST': 'Indigenous Areas - 2021',
  'IREG_2021_AUST': 'Indigenous Regions - 2021',
  'LGA_2023_AUST': 'Local Government Areas - 2023',
  'LGA_2022_AUST': 'Local Government Areas - 2022',
  'LGA_2021_AUST': 'Local Government Areas - 2021',
  'SED_2022_AUST': 'State Electoral Divisions - 2022',
  'SED_2021_AUST': 'State Electoral Divisions - 2021',
  'CED_2021_AUST': 'Commonwealth Electoral Divisions - 2021',
  'POA_2021_AUST': 'Postal Areas - 2021',
  'TR_2021_AUST': 'Tourism Regions - 2021',
  'ADD_2021_AUST': 'Australian Drainage Divisions - 2021',
  'SAL_2021_AUST': 'Suburbs and Localities - 2021',
  'MB_DZN_2021_AUST': 'Destination Zones - 2021',
  'DZN_SA2_2021_AUST': 'Destination Zones to Statistical Areas Level 2 - 2021',
  'SUA_2021_AUST': 'Significant Urban Areas - 2021',
  'UCL_SOSR_SOS_2021_AUST': 'Urban Centres and Localities, Section of State and Section of State Range - 2021',
  'SUA_association_2016_2021': 'Significant Urban Area association - 2016 to 2021',
  'UCL_association_2016_2021': 'Urban Centre and Locality association - 2016 to 2021',
  'RA_2021_AUST': 'Remoteness Areas - 2021'
}

# !cd AusGeo/data/mb-allocation && ls -lh | sort -k 5,5 -h

# ['MB_2021_AUST',
# 'SA1_2021_AUST',
# 'SA2_2021_AUST',
# 'SA3_2021_AUST',
# 'SA4_2021_AUST',
# 'GCCSA_2021_AUST',
# 'STE_2021_AUST',
# 'AUS_2021_AUST',
# 'INDIGENOUS_STRUCTURE_ALLOCATION_2021',
# 'ILOC_2021_AUST',
# 'IARE_2021_AUST',
# 'IREG_2021_AUST',
# 'LGA_2023_AUST',
# 'LGA_2022_AUST',
# 'LGA_2021_AUST',
# 'SED_2022_AUST',
# 'SED_2021_AUST',
# 'CED_2021_AUST',
# 'POA_2021_AUST',
# 'TR_2021_AUST',
# 'ADD_2021_AUST',
# 'SAL_2021_AUST',
# 'MB_DZN_2021_AUST',
# 'DZN_SA2_2021_AUST',
# 'SUA_2021_AUST',
# 'UCL_SOSR_SOS_2021_AUST',
# 'SUA_association_2016_2021',
# 'UCL_association_2016_2021',
# 'RA_2021_AUST']


# Download the files from Google Colab if this notebook is running on Google Colab

# import os
# from google.colab import files

# # Define the folder to be downloaded
# folder_to_download = '/content/AusGeo/data/mb-allocation'

# # Get the list of files in the folder
# files_to_download = os.listdir(folder_to_download)

# # Iterate over each file and download it
# for file_name in files_to_download:
#     file_path = os.path.join(folder_to_download, file_name)
#     files.download(file_path)

