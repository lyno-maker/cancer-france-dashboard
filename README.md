# Cancer in France: where is the risk highest? (Streamlit)

Individual student project — EFREI Paris — Data Storytelling Dashboard 2026 (#EFREIDataStories2026)
Author: **Lyne NGOUOWA** — group BIO
Deployed app: https://cancer-france-dashboard-5vnb6ks3mqdrfgegwyq3yg.streamlit.app/ · Repository: https://github.com/lyno-maker/cancer-france-dashboard · 
Demo video:https://www.youtube.com/watch?v=TNGax8GEysc

Interactive dashboard on territorial inequalities in cancer incidence in France (age-standardised rates, Francim registry data).

## Data
- **Dataset**: "Observed incidence of invasive tumours in the départements covered by the Francim registries between 1988-1992 and 2018-2022" — producer: Institut National du Cancer (INCa), published on data.gouv.fr: [**DATA_GOUV_URL**](https://www.data.gouv.fr/datasets/incidence-observee-des-tumeurs-invasives-dans-les-departements-couverts-par-les-registres-francim-entre-1988-1992-et-2018-2022). Last updated 16 March 2026.
- **License**: Other (Public Domain), as stated on the data.gouv.fr page.
- **Indicator used**: incidence rate standardised on the world population age structure (`ratemonde`), per 100,000 person-years.
- **Coverage**: 21 départements covered by a registry, in 5-year periods. Overseas départements appear in the rankings but not on the map (the boundaries file only covers metropolitan France).
- The CSV is downloaded automatically on first run into `data/raw.csv` (cache), from the Santé publique France Odissé portal. Map boundaries: `gregoiredavid/france-geojson`. Source data labels (cancer sites) are in French.

## Run locally
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python -m streamlit run app.py
```
If the download fails, download the CSV manually and upload it through the app sidebar.

## Structure
- `app.py`: filters (sidebar) and orchestration
- `sections/`: intro, overview (KPIs + map), deep_dives (ranking, trends, distribution), conclusions
- `utils/`: `io.py` (loading + cache), `prep.py` (column detection, cleaning, validation), `viz.py` (charts)
- `data/`: local cache (not versioned)

## Narrative
Hook → Context → Insights (map, ranking, trend, distribution) → Data quality and limitations → Implications.

## Methodological choices
- The mean rate is a simple average of départements, not weighted by population.
- The KPI change compares the same départements between the first and the last selected period.
- When several periods are selected, the map and ranking show the average over those periods.

## Limitations
Partial coverage (registries, 21 départements), no overseas départements on the map, associations are not causal (screening, behaviours and environment play a role). Aggregated data: no re-identification risk. Constant `SEED = 42` in `utils/io.py`.
