let
    ReadSales = (fileName as text) as table =>
        let
            Source = Csv.Document(File.Contents(DataFolder & fileName),
                [Delimiter=",", Encoding=1252, QuoteStyle=QuoteStyle.Csv]),
            Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
            Types = Table.TransformColumnTypes(Headers,
                {{"OrderDate",type date},{"StockDate",type date},{"OrderNumber",type text},
                 {"ProductKey",Int64.Type},{"CustomerKey",Int64.Type},{"TerritoryKey",Int64.Type},
                 {"OrderLineItem",Int64.Type},{"OrderQuantity",Int64.Type}}, "en-US")
        in Types,
    AllYears = Table.Combine({ReadSales("Sales Data 2020.csv"),
                               ReadSales("Sales Data 2021.csv"),
                               ReadSales("Sales Data 2022.csv")}),
    AddLineID = Table.AddIndexColumn(AllYears, "SalesLineKey", 1, 1, Int64.Type)
in
    AddLineID
