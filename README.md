# Analysis of Australian Postcodes and GeoJson Data

This repository contains the code and data for the analysis of Australian geographical data, including mesh blocks, postcodes, and suburbs GeoJSON data. The analysis is done using Python, and the main data source is the Australian Bureau of Statistics (ABS) and other open data sources.

## Data sources

- Australian Statistical Geography Standard (ASGS) Edition 3
    - https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026

- Digital boundary files:
    - https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files
        - Suburbs boundary files can be found at: Non ABS Structures > Suburbs and Localities
        - Local Government Areas boundary files can be found at: Non ABS Structures > Local Government Areas
        - Postcodes boundary files can be found at: Non ABS Structures > Postal Areas

- ABS Maps:
    - https://maps.abs.gov.au/
    - https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/abs-maps

- Suburbs, Postcodes, Local Government Area boundaries:
    - Tony Wright's dataset of suburbs' GeoJSON and postcodes: https://github.com/tonywr71/GeoJson-Data

- Postcodes: 
    - Australia Post's Postcode Finder: https://auspost.com.au/postcode
    - Matthew Proctor's Postcodes dataset: https://www.matthewproctor.com/australian_postcodes


## Instructions

This repository has downloaded data from ABS and uploaded it to the `data` directory. All rights to the data belong to the ABS.

Instructions for loading the downloaded data from this repository are provided in the load-data.ipynb notebook.