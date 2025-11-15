# Engines Safety in Western Commercial Aviation (2000--2025)

## 1. Introduction

This project analyses the safety of aircraft engines used in western
commercial aviation over the last 25 years. The study combines multiple
fleet databases with web‑scraped incident records, merging them into a
unified analytical dataset to evaluate patterns, frequencies and risk
indicators related to engine failures.

The scope was adapted during the project due to access limitations to
proprietary flight information databases. The team pivoted from a maintenance
benchmark to a safety‑focused study using publicly accessible sources.

## 2. Data Sources

### Fleet & Aircraft Data

-   **9 independent CSV files** consolidated into a single DataFrame\
-   Included variables: aircraft model, engine manufacturer, operator,
    country, delivery year, age, status.

### Incident Data (Web Scraping)

-   Source: **Aviation Safety Network (ASN)**\
-   Scraped yearly engine‑related incidents for the last 25 years\
-   Extracted: date, aircraft registration, aircraft type, engine info,
    incident classification

### Comments on the Data

**Strengths** 
- Large historical window (2000--2025)
- Real incidents directly tied to individual aircraft
- Cross‑referencing by aircraft registration increases accuracy

**Challenges & Weaknesses** 
- Inconsistent aircraft registration formats
- Country names not standardized (manual ISO corrections)
- Missing delivery years
- Unstructured incident descriptions
- Web scraping limitations & dynamic pages

## 3. Questions to Answer

### Fleet Structure & Evolution

-   How has the western fleet evolved?
-   What patterns appear during major events like COVID‑19?

**Conclusion:**\
Deliveries reduced during COVID‑19, Boeing showed a significant decline
in 2019--2020 following the 737 MAX grounding.

### Engine Safety

-   What % of the active fleet experienced an engine‑related failure?
-   Are certain engine manufacturers associated with higher incident
    rates?
-   Are specific aircraft models over‑represented?

**Conclusion:**\
The percentage of aircraft with recorded engine‑failure incidents is
small compared with total fleet volume, but differences between
manufacturers are visible when normalized.


## 4. Methodology

### 4.1 Data Wrangling & Cleaning

-   **Merge of 9 CSV files**
-   **Standardized ISO‑3 country codes**
-   **Missing delivery years:** imputed as *current year -- aircraft age*
-   **Normalization of engine manufacturers:** reduced to 4 canonical suppliers
-   **Created dataset of in‑service aircraft only**

### 4.2 Web Scraping Pipeline

-   Iterated through incident listing pages\
-   Saved raw pages into **JSON cache**\
-   Converted JSON to pandas DataFrame\
-   Normalized date formats and extracted year column\
-   Standardized aircraft registrations to match fleet database\
-   Inner-joined incidents to fleet data on registration (primary key)

### 4.3 Exploratory Data Analysis

-   Engines vs incidents (2000--2025)\
-   Fleet age distribution\
-   Deliveries per year\
-   Trends per OEM (Boeing vs Airbus)\
-   Breakdown of incidents per engine manufacturer

## 5. Conclusions & Insights

-   The % of the active fleet with at least one engine‑failure incident
    remains low overall.\
-   Normalization per manufacturer reveals significant differences in
    exposure and reliability perception.\
-   Boeing's deliveries were strongly affected by COVID‑19 and the 737
    MAX crisis, while Airbus maintained stable growth.\
-   Web‑scraped incident data effectively complements fleet databases
    when proprietary data is not accessible.\
-   The project demonstrates the complexity of consolidating
    heterogeneous aviation datasets at registration level.

------------------------------------------------------------------------

**Authors:**\
Marlene Alcobendas & Iván Prieto
