# Yahoo-Data-Crawling-and-Analysis
Supply Chain Business Intelligence (BI) tool

##  Project Description
This project is a data-driven **Supply Chain Business Intelligence (BI) tool** designed for procurement managers and logistics analysts to monitor global supply chain asset costs and commodity price volatility in real-time.

In global trade, sudden fluctuations in raw materials (e.g., Crude Oil, Copper) or shipping costs heavily impact corporate profit margins. This tool allows users to input any global market ticker symbol (such as `CL=F` for Crude Oil, `BDRY` for Shipping Freight, or `AAPL` for tech supply chains) to dynamically fetch, clean, and analyze historical data from the past month.

The program automatically calculates critical supply chain risk metrics, generates an analytical text report, and exports a customized visualization chart (`supply_trend.png`) to help enterprises optimize their purchasing frequencies and mitigate supply risk.

---

##  Project Structure

* `project.py`: The main program containing the core logic: user input handling, API request configuration, execution of data pipelines, and chart visualization.
* `test_project.py`: The test suite containing robust unit tests powered by `pytest` to verify the logic of all data-processing and analytics functions without relying on live internet connections.
* `requirements.txt`: A list of third-party Python libraries (`requests`, `pandas`, `matplotlib`) required to run the tool.
* `supply_trend.png`: A dynamically updated line chart displaying the 30-day price trend of the specified supply chain asset.

---

## Core Functions Explained

### 1. `clean_data(raw_data)`
* **What it does:** This function handles the initial ETL (Extract, Transform, Load) phase. It accepts the raw, nested JSON dictionary directly fetched from the Yahoo Finance API, digs out the synchronized `timestamp` and `close` price arrays, and converts them into a clean, well-structured Pandas DataFrame.
* **Data Cleaning:** It automatically drops rows with missing data (null values caused by market holidays/closures) and converts Unix timestamps into human-readable `YYYY-MM-DD` date formats.

### 2. `calculate_data(cf)`
* **What it does:** Performs commercial financial arithmetic on the cleaned DataFrame. It calculates the maximum price, minimum price, and the most recent closing price over the 30-day period. Crucially, it computes the net price change percentage (`price_change_pct`) from the start of the month to the end, identifying cost trends.

### 3. `risk_report(price_change_pct)`
* **What it does:** Implements a rule-based logic to evaluate supply chain purchasing risks.
    * If costs surge past **+8%**, it triggers a `HIGH RISK (Red)` warning, advising managers to find alternative suppliers.
    * If costs drop below **-8%**, it indicates a cost-saving window, advising managers to increase inventory.
    * Otherwise, it reports a `STABLE (Yellow)` risk status.

---

##  How to Run the Project

1. Install all dependencies from the root directory:
   pip install -r requirements.txt

2. Execute the main program:
   python project.py

3. Enter a valid asset ticker when prompted (e.g., CL=F for Crude Oil or BDRY for shipping carrier).

---

##  How to Run Tests

To ensure the reliability of the data processing pipeline, run the automated test suite using `pytest`:
pytest test_project.py

