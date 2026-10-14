# Portfolio audit and verification

## Improvements

- Verified all 14 project folders on the connected GitHub repository.
- Added four runnable Jupyter notebooks, associated requirements, and the public Tips teaching dataset.
- Added GitHub Actions workflow `.github/workflows/python-checks.yml` and seven offline automated Python tests.
- Made the bike example import-safe by moving its demonstration into `demo()` and a `__main__` guard.
- Fixed AdventureWorks DAX gross margin to reference the defined `[Total Gross Profit]` measure.
- Published a Power BI reconstruction guide, DAX measures, a sample M query and relationships specification.

## Automated test coverage

Tests cover Python date validation, bank transactions, bike state changes, NumPy output, pandas cleaning, notebook syntax, and a synthetic-data regression pipeline. Tests use no real customer records and no network access.

## Important limitations

- Tests do not verify a native Power BI PBIX, actual SQL server deployment, or MongoDB runtime in production.
- Notebook execution may require packages and/or the datasets linked in each project.
- Original customer-level data from previous course tasks is excluded; obtain authorized source copies if reconstructing BI reports.
- Some source projects are course exercises; do not treat them as independently validated deployed systems.

## Future improvements

Add reproducible demonstration screenshots and executed notebooks, validate SQL and MongoDB code against live local engines, and document any graduate group project only after confirming co-author/publication permission.
