# Power BI reconstruction guide

These are implementation files for a training project, **not a native PBIX**.

1. Obtain the original educational AdventureWorks CSV extracts from an authorized source. Customer-level CSV exports are deliberately **excluded** from this public repository.
2. Create a `DataFolder` text parameter in Power Query containing the CSV directory path (including its final slash).
3. Import dimensions: customers, products, calendar, territories. Combine 2020, 2021 and 2022 sales CSVs using [Power Query M](../power_query/fact_sales.m). Load returns separately.
4. Create the single-direction, one-to-many relationships in [relationships.csv](relationships.csv).
5. Add each calculated column and DAX measure separately from [the DAX folder](../dax). `Gross Margin %` is defined using `[Total Gross Profit]` — a corrected reference.
6. Add a line chart by date, a bar chart by category, pie chart, KPI cards, year/category/income slicers and a territory map.
7. Check the totals against the original CSVs before presenting the finished PBIX.

Gross profit is revenue less standard product cost before tax, operating costs and refunds. The standalone HTML demonstration in the original course project should not be described as a Power BI PBIX file.
