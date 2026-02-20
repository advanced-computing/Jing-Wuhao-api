# Five Takeaways
## Jing Bu, Wuhao Xia

Here are five key takeaways and findings based on the data profiling visualizations.

### 1. Demographic Concentration
The dataset reveals a significant demographic skew in the arrested population. Males account for the vast majority of arrests at 80%, compared to females at 20%. Furthermore, the primary age group involved is 25-44 years old, which constitutes 60% of the records, followed by the 45-64 (19%) and 18-24 (16%)s.

### 2. Severity and Common Charges
The majority of arrests are for lower-level offenses. Looking at the Law Category Code, Misdemeanors make up 60% of the charges, while Felonies ('F') account for 39%. The top specific offenses align with this, being "ASSAULT 3 & RELATED OFFENSES" (18%) and "PETIT LARCENY" (11%), followed by "FELONY ASSAULT" (10%).

### 3. Geospatial Anomalies
While location tracking is mostly complete, there are data quality issues in the coordinates that will require cleaning before mapping. Both the latitude and longitude columns have a small number of missing values (4 records). More importantly, the minimum values for latitude and longitude are 0.0, which indicates incorrect or default zero-filled geospatial entries that will plot off the coast of Africa (Null Island) if not filtered out.

### 4. Jurisdictional Dominance
The jurisdiction_code distribution is heavily dominated by a single category. Code 0 accounts for nearly all the records, as seen by the massive single spike in the histogram. The remaining 16 jurisdiction codes make up a negligible fraction of the total arrests.

### 5. Temporal Snapshot
The arrest_date profiling shows that this dataset may be a specific time-bound snapshot rather than a uniform yearly dataset. The top three most frequent arrest dates are December 26, 27, and 28 of 2024, which together account for 41% of the data distribution shown. If you are intending to do a longitudinal analysis, you will need to verify if this dataset represents only a few weeks of data or if there's a heavy skew.