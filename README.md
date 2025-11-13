# Benchmark of Aircraft: Safety & Fleet Analysis

## 📌 Introduction
This project provides a comprehensive benchmark of aircraft manufacturers, engine manufacturers and operator fleets worldwide.  
By integrating Aircraft Worldwide (AW) fleet data with Aviation Safety Network (ASN) engine-related events, the goal is to understand patterns in fleet composition, manufacturer combinations and engine safety performance.

## 📂 Data Sources

### 1. Aircraft Worldwide (AW) Dataset
Contains global aircraft fleet information including registration, operator, manufacturer, engine manufacturer and country codes.

**Strengths**
- High granularity  
- Strong coverage of fleet data  

**Weaknesses / Challenges**
- Inconsistent formats  
- Missing values  
- Duplicates  

### 2. Aviation Safety Network (ASN)
Engine-related events dataset requiring keyword filtering and date normalization.

## ❓ Questions to Answer

### A. Fleet Composition & Structure
1. Which countries operate the largest fleets?  
**Conclusion:** Fleet size correlates with economic development and airline presence.

2. Top aircraft–engine manufacturer combinations by country.  
**Conclusion:** Regional preferences appear clearly.

### B. Engine Safety Analysis
3. Percentage of each engine manufacturer’s fleet in ASN events.  
**Conclusion:** Very low ratios (<1%), confirming engine reliability.

4. Are some models overrepresented?  
**Conclusion:** No anomalies beyond fleet-size correlation.

### C. Country Safety Patterns
5. Countries with higher proportions of ASN-linked aircraft.  
**Conclusion:** Patterns reflect fleet age or traffic volume.

## ⚙️ Methodology

### 1. Data Loading
- CSV/JSONL import  
- Separator checks  
- Encoding fixes  

### 2. Cleaning
- Text normalization  
- Manufacturer mappings  
- Duplicate removal  
- Date parsing  
- Creation of `year` column  

### 3. Merging
- Normalized registrations  
- Left join AW ↔ ASN  
- Created `asn_engine_flag`  

### 4. Analysis
- Groupbys  
- Percentages & ratios  
- Plotly geo-scatter, bar charts and combinations plots  

## 📊 Conclusions
- Engine-related events are extremely rare globally  
- No manufacturer shows abnormal incident rates  
- Most differences reflect fleet size or operational density  
- Text normalization was the biggest challenge  