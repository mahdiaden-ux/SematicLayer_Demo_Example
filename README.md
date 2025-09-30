# GA4 BigQuery Semantic Layer

This project provides a semantic layer on top of Google Analytics 4 (GA4) event data stored in Google BigQuery. It uses the `boring-semantic-layer` library to define a semantic model and exposes it through a Model-View-Controller Protocol (MCP) server.

This allows for consistent and simplified querying of your GA4 data from compatible client applications (like Cursor).

## Features

*   Connects to your Google BigQuery project and dataset.
*   Defines a semantic model for GA4 event data (`ga4_events_sm`).
*   Exposes dimensions like `event_date` and `user_pseudo_id`.
*   Exposes measures like `event_count`.
*   Runs an MCP server to serve the semantic model, making it available for querying.

## Prerequisites

*   Python 3.11 or newer.
*   Access to a Google Cloud project with the BigQuery API enabled.
*   GA4 event data exported to a BigQuery table.
*   Google Cloud SDK installed and authenticated on your local machine. You can authenticate by running:
    ```bash
    gcloud auth application-default login
    ```

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd measurecamp-london-bigqery-mcp
    ```

2.  **Install dependencies:**
    The project uses `uv` to manage and run the Python environment. The required dependencies are listed at the top of the `layer.py` file. `uv` will install them automatically when you run the server. If you don't have `uv`, you can install it with:
    ```bash
    pip install uv
    ```

## Configuration

Before running the server, you need to configure it to point to your BigQuery data. Open the `layer.py` file and modify the following lines:

1.  **Update BigQuery Connection:**
    Change `project_id` and `dataset_id` to match your Google Cloud setup.

    ```python
    con = ibis.bigquery.connect(
        project_id="your-gcp-project-id",
        dataset_id="your_bigquery_dataset_id",
    )
    ```

2.  **Update Table Name:**
    Change the table name to your GA4 events table.
    ```python
    ga4_table = con.table("events_YYYYMMDD")
    ```

3.  **Update Primary Key:**
    The current `primary_key` in the `ga4_events_sm` model is set to `"code"`, which is likely a remnant from an example. You should update this to a unique key for your events table or remove it if one is not applicable. A combination of `user_pseudo_id` and `event_timestamp` is often used to uniquely identify an event, but `boring-semantic-layer` currently supports single-column primary keys. For now, you can remove the line.

## Running the Server

Once configured, you can start the MCP server by running the following command in your terminal:

```bash
uv run layer.py
```

The server will start and listen for connections from MCP clients.

## Usage with an MCP Client (e.g., Cursor)

To connect to this server from an MCP-compatible editor like Cursor, you need to configure it as an MCP server.

1.  In Cursor, create or open the `.cursor/mcp.json` file in your project's root directory.
2.  Add the following configuration to the `mcpServers` object:

    ```json
    {
        "mcpServers": {
            "ga4-semantic-layer": {
                "command": "uv run layer.py",
                "language": "python"
            }
        }
    }
    ```

3.  Reload Cursor. You can now use `@ga4-semantic-layer` in the chat to query your semantic model. For example:
    > @ga4-semantic-layer How many events were there per day?

This will query your BigQuery table through the semantic layer and return the results.

