# Architecture sketches for selected projects

These diagrams summarize the relationships present in the course projects. They are conceptual aids, not an automatic migration or a Power BI `.pbix` export.

## Retail BI — star schema

```mermaid
erDiagram
    DimProducts ||--o{ FactSales : "Product ID"
    DimCustomers ||--o{ FactSales : "Customer ID"
    DimDate ||--o{ FactSales : "Date Key"
    FactSales ||--|| FactFeedback : "Invoice ID"
    DimProducts {
        int Product_ID PK
        string Category
        float Cost
    }
    DimCustomers {
        int Customer_ID PK
        string Region
        string Customer_Type
    }
    DimDate {
        int Date_Key PK
        date Date
    }
    FactSales {
        int Invoice_ID PK
        int Product_ID FK
        int Customer_ID FK
        int Date_Key FK
        float Revenue
        float Profit
    }
    FactFeedback {
        int Invoice_ID FK
        float Service_Rating
        float Quality_Rating
    }
```

Data classification is based on linked product/customer dimension tables. Refer to [retail DAX definitions](../05-business-intelligence/powerbi-store-satisfaction/dax/measures_and_columns.txt). Business metrics come from an educational dataset; the underlying raw customer records are withheld from this public repository.

## AdventureWorks BI — dimensional model

```mermaid
erDiagram
    DimCalendar ||--o{ FactSales : "OrderDate"
    DimCalendar ||--o{ FactReturns : "ReturnDate"
    DimCustomers ||--o{ FactSales : "CustomerKey"
    DimProducts ||--o{ FactSales : "ProductKey"
    DimProducts ||--o{ FactReturns : "ProductKey"
    DimTerritories ||--o{ FactSales : "TerritoryKey"
    DimTerritories ||--o{ FactReturns : "TerritoryKey"
```

In the model, the calculated column is `FactSales[Gross Profit]` and the associated total measure is `[Total Gross Profit]`; `[Gross Margin %]` correctly references the latter. See the [implementation guide](../05-business-intelligence/powerbi-adventureworks-sales/docs/implementation.md).

## Electronic library — MySQL relational model

```mermaid
erDiagram
    authors ||--o{ books : writes
    books ||--o{ borrowings : loaned_in
    members ||--o{ borrowings : makes
```

[Source SQL](../04-databases/mysql-electronic-library/sql/library_management.sql) includes primary keys, foreign keys and stored procedures. This is an educational local schema, not a deployed borrowing service.

## School management — many-to-many relationships

```mermaid
erDiagram
    teachers ||--o{ teacher_students : teaches
    students ||--o{ teacher_students : attends
    students ||--o{ student_subjects : takes
    school_subjects ||--o{ student_subjects : includes
    school_subjects ||--o{ teachers : assigned_to
```

The school course also uses renamed tables across SQL levels. Run the [combined script](../04-databases/mysql-school-management/sql/school_management_levels_1_to_3.sql) in sequence on a disposable test database.
