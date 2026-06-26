# Research Ideas

Data sources: NDCU Daily (district-level cumulative cases) and NDCU Weekly (district cases with YoY comparisons, deaths by district/age/sex, high-risk MOH areas with per-100k incidence, sentinel hospital admissions).

---

## Ideas (prioritized by life-saving potential)

### 1. Automated epidemic threshold alerts per district ⚡ (highest priority)

Erandi et al. define outbreak threshold as the 5-year moving average for the same epidemiological week. The weekly data already provides `n_this_year_this_week` vs `n_last_year_this_week` and cumulative figures. Build a per-district threshold computed from historical NDCU data (2019–2025) and automatically flag districts exceeding it each week — enabling health authorities to mobilize vector control before case loads peak. Currently, RDHS relies on a static 5-year average that misses outbreak magnitude (Erandi Fig. 8).

### 2. 4-week-ahead outbreak forecast using climate lags (GLM)

Erandi et al. show that dengue in Colombo correlates with rainfall at 10-week lag, max temperature at 16-week lag, min temperature at 13-week lag. Using weekly NDCU case data as the dependent variable and publicly available Sri Lanka Meteorological Department data (rainfall, temperature) as predictors, implement the log-linear GLM: `log(D_t + 1) = β₀ + β₁R_{t-10} + β₂MT_{t-16} + β₃mT_{t-13} + β₄D_{t-4}`. This produces 1-month-advance alerts for each district — enough lead time for targeted fogging and community clean-up campaigns.

### 3. Sentinel hospital surge as a leading indicator

The weekly `sentinel_hospitals.tsv` tracks hospital admissions before community surveillance reflects them. Build an index of week-over-week hospital admission growth rates (e.g., TH-Ratnapura jumped from 51→122 in one week). A threshold on this index predicts district-level outbreak peaks 1–2 weeks earlier than NDCU notification data — critical for triage and bed preparation.

### 4. Getis-Ord Gi* hot spot analysis at MOH-area level

Sun et al. apply Getis-Ord Gi*spatial statistics to district-level data. The `high_risk_moh_areas.tsv` already provides population-normalized incidence (~100 MOH areas) and `moh.topojson` provides spatial geometry. Applying Gi* with spatial weights derived from shared boundaries (Thiessen polygons as in Sun et al.) identifies statistically significant hot spots vs the current ad-hoc "high risk" list — enabling focalized interventions rather than district-wide campaigns, saving resources and lives.

### 5. Mortality risk cross-tabulation: who is dying and where

The `deaths_by_age_and_sex.tsv` shows 18 female vs 6 male deaths (3:1 ratio, unexpected). `deaths_by_district.tsv` shows Colombo (7) and Gampaha (5) dominate. Cross-tabulating age-sex mortality with high-incidence MOH areas identifies demographic and geographic pockets of excess case-fatality rate — actionable for targeted clinical training and hospital resource prioritization. (Piyatilake identifies high population density as a key risk factor; mortality concentration in urban Colombo/Gampaha aligns with this.)

### 6. Year-over-year acceleration detection

The weekly data includes `n_this_year_this_week` and `n_last_year_this_week` per district. Compute the ratio and flag districts where 2026 case pace exceeds 2025 by more than 2 standard deviations from the historical inter-year variance. This is a model-free early warning requiring no meteorological data — implementable immediately. Current data shows Colombo (1208 vs 292), Matara (468 vs 43), and Galle (275 vs 43) already at 4–10× last year's pace.

### 7. Data-driven IR compartmental model for 4-week forecasts (per district)

Erandi et al. 2021 show a quasi-equilibrium IR model with time-varying per-capita vector density `n(t)` driven by climate achieves >75% accuracy 4 weeks ahead in CMC. Extend this to all 25 districts using the weekly NDCU data as the infected population time series. Fit `n(t)` as a Fourier function calibrated to each district's rainfall pattern (26-week periodicity confirmed). Districts like Matara and Galle showing extreme YoY surges in 2026 are highest-priority candidates.

### 8. Spatial-temporal cluster detection across consecutive weeks

Sun et al. use Kulldorff's spatial scan statistic to detect clusters in space and time simultaneously. With weekly MOH-area data across 2024–2026, run a cylindrical space-time scan (population as control) to detect emerging outbreak clusters before they reach epidemic scale. The `moh.topojson` provides the spatial component. Early cluster detection enables cooperative multi-district control responses (Sun et al. note that single-district control fails if neighboring districts don't act).

### 9. Fuzzy multidimensional risk scoring at MOH area level

Piyatilake et al. find that population movements and garbage collection are the top-weighted risk factors (ahead of climate variables). The MOH-level data already has population figures. Augmenting with: (a) urbanization rate from census data, (b) garbage collection data from local authorities, (c) population movement proxies (mobile data or commuter flow estimates) would enable a full fuzzy AHP risk score per MOH area — producing a forward-looking risk map vs the current reactive case-count map. Most districts are predicted to reach moderate risk by 2022 (paper forecast); 2026 data can validate and update this.

### 10. District-level ARIMAX forecasting with climate covariates

Sun et al. build ARIMAX models per district using monthly data. The weekly NDCU data enables weekly-resolution ARIMAX with meteorological covariates, producing rolling 4–8-week forecasts per district. Districts in the second (cold-spot) cluster — Anuradhapura, Moneragala, Nuwara Eliya, Puttalam — show low but non-climate-driven incidence; ARIMAX without climate terms may outperform GLM there, per Sun et al.'s finding that non-climate factors dominate those regions.

---

## Appendix 1: Fillable Data Gaps

- **Meteorological data** (rainfall, max/min temperature, humidity, wind speed) not in current dataset — needed for ideas 2, 7, 9, 10. Available from Sri Lanka Meteorological Department.
- **Historical NDCU weekly series** (pre-2025) — needed for ideas 1, 7, 8, 10. Older PDFs available from NDCU archive.
- **Garbage collection / urbanization / population movement data** — needed for idea 9.
- **Serotype surveillance data** — not in NDCU reports but relevant: serotype shifts drive 2–3-year epidemic cycles (Erandi 2021).

---

## References

1. Erandi et al. (2021) — [Dengue outbreak prediction model for urban Colombo using meteorological data](research_papers/[2021%20Erandi%20et%20al]%20Dengue%20outbreak%20prediction%20model%20for%20urban%20Colombo%20using%20meteorological%20data.pdf)
2. Erandi et al. (2021) — [Analysis and forecast of dengue incidence in urban Colombo, Sri Lanka](research_papers/[2021%20Erandi%20et%20al]%20Analysis%20and%20forecast%20of%20dengue%20incidence%20in%20urban%20Colombo,%20Sri%20Lanka.pdf)
3. Sun et al. (2017) — [Spatial-temporal distribution of dengue and climate characteristics for two clusters in Sri Lanka from 2012 to 2016](research_papers/[2017%20Sun%20et%20al]%20Spatial-temporal%20distribution%20of%20dengue%20and%20climate%20characteristics%20for%20two%20clusters%20in%20Sri%20Lanka%20from%202012%20to%202016.pdf)
4. Piyatilake et al. (2020) — [Fuzzy Multidimensional Model to Cluster Dengue Risk in Sri Lanka](research_papers/[2020%20Piyatilake%20et%20al]%20Fuzzy%20Multidimensional%20Model%20to%20Cluster%20Dengue%20Risk%20in%20Sri%20Lanka.pdf)
