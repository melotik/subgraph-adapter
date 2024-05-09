# Subgraph Adapter

Using python to poll a subgraph and dumping the data into a csv

> Note: this output file is not 100% accurate, the updated subgraph with bug fixes is not syncing (issue with the graph)

## How to Use

Set env vars
```bash
cp .env.example .env
source .env
```
> Get your api key using these docs: https://thegraph.com/docs/en/querying/managing-api-keys/

Setup (MacOS)
```bash
python3 -m venv subgraph
source subgraph/bin/activate
pip install -r requirements.txt
```

Run
```bash
python3 fetch_positions.py <YOUR_ACCOUNT_ID>
```

Shut down
```bash
deactivate
```
