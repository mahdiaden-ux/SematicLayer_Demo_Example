# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "boring-semantic-layer[examples] >= 0.1.9",
#     "boring-semantic-layer[mcp] >= 0.1.9",
#     "boring-semantic-layer[viz-altair] >= 0.1.9",
#     "ibis-framework[bigquery]>=10.8.0",
# ]
# ///

"""
Basic MCP server example using semantic models.

This example demonstrates how to create an MCP server that exposes semantic models
for querying flight and carrier data. The server provides tools for:
- Listing available models
- Getting model metadata
- Querying models with dimensions, measures, and filters
- Getting time ranges for time-series data

Usage:
    1: add the following config to the .cursor/mcp.json file:
    {
        "mcpServers": {
            "flight-semantic-layer": {
                "command": "uv run  mcp_basic_example.py",
                "language": "python"
            }
        }
    }

The server will start and listen for MCP connections.

"""

from boring_semantic_layer import MCPSemanticModel, SemanticModel, Join
import ibis

con = ibis.bigquery.connect(
    project_id="moritz-test-projekt",
    dataset_id="analytics_474874421",
)

ga4_table = con.table("events_20250918")

ga4_events_sm = SemanticModel(
    name="Google Analytics 4 Events",
    description="Every row resembles an event in GA4",
    table=ga4_table,
    dimensions={
        "event_date": lambda t: t.event_date,
        "user_pseudo_id": lambda t: t.user_pseudo_id
    },
    measures={
        "event_count": lambda t: t.count(),
    },
)



server = MCPSemanticModel(
    models={"ga4_events":ga4_events_sm},
    name="Our Google Analytics 4 event table",
)

if __name__ == "__main__":
    server.run()