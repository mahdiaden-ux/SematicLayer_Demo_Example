# layer.py
import os
import ibis
from boring_semantic_layer import (
    SemanticModel,
    MCPSemanticModel,
    DimensionSpec,
    MeasureSpec,
)

# configuration via env vars
PROJECT = os.environ.get("BQ_PROJECT", "")
DATASET = os.environ.get("BQ_DATASET", "")
TABLE   = os.environ.get("BQ_TABLE", "")

# connect to BigQuery via Ibis
# works with ADC or GOOGLE_APPLICATION_CREDENTIALS
con = ibis.bigquery.connect(project_id=PROJECT, dataset_id=DATASET)
ga4_tbl = con.table(TABLE)

# define semantic model
ga4_events_sm = SemanticModel(
    name="ga4_events",
    table=ga4_tbl,
    description="GA4 events (flattened view) for analytics queries",
    dimensions={
        "event_date": DimensionSpec(
            expr=lambda t: t['event_date'],  # use new column API
            description="Event date (YYYYMMDD string)"
        ),
        "event_name": DimensionSpec(
            expr=lambda t: t['event_name'],
            description="GA4 event name"
        ),
        "user_pseudo_id": DimensionSpec(
            expr=lambda t: t['user_pseudo_id'],
            description="GA4 user pseudo id"
        ),
        "page_location": DimensionSpec(
            expr=lambda t: t['page_location'],
            description="page_location event param"
        ),
    },
    measures={
        "event_count": MeasureSpec(
            expr=lambda t: t.count(),
            description="Total number of events"
        ),
        "unique_users": MeasureSpec(
            expr=lambda t: t['user_pseudo_id'].nunique(),  # modern Ibis syntax
            description="Count of unique user_pseudo_id"
        ),
    },
    primary_key="event_id",  # make sure your table has this column
)

# create MCP server
mcp_server = MCPSemanticModel(
    models={"ga4_events": ga4_events_sm},
    name="GA4 BigQuery Semantic Layer"
)

if __name__ == "__main__":
    # run over stdio
    mcp_server.run(transport="stdio")
