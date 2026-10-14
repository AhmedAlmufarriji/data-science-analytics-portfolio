# AdventureWorks Sales & Profit Analysis

A Power BI training data model and associated Power Query / DAX implementation files.

**Stack:** Power BI Desktop, DAX, Power Query M

## Model and measures

- Dimension tables for calendar, customers, products and sales territories; fact tables for sales and returns.
- Calculated sales revenue and gross profit, order counts, margin, return rates and conditional bar colors.
- The gross-margin calculation has been corrected to reference the defined `[Total Gross Profit]` measure.

**What is published:** DAX, a sample Power Query M file, relationship specifications and a [reconstruction guide](docs/implementation.md).  
**What is not published:** customer-level raw CSV exports and any native Power BI `.pbix` file.

Any HTML visualization created during the exercise is a separate prototype and should not be represented as a Power BI export.

## How to get started

```bash
Open Power BI Desktop and follow docs/implementation.md
```

[DAX measures](dax/measures.dax) · [Relationships](docs/relationships.csv)
