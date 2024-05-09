import argparse
import os
import requests
import csv

# Fetch the access token from the environment variable
access_token = os.getenv("ACCESS_TOKEN")
if not access_token:
    raise ValueError("The ACCESS_TOKEN environment variable is not set!")

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Fetch GraphQL data for an account and save it to CSV.")
parser.add_argument("account", type=str, help="The account ID to query.")
args = parser.parse_args()
account_id = args.account

# GraphQL endpoint - https://thegraph.com/explorer/subgraphs/H3XsUaJ4mTTP3qp2TEPkBY2oqr6ZcKVrfQu9aj8EMFGm?view=Overview&chain=arbitrum-one
url = f"https://gateway-arbitrum.network.thegraph.com/api/{access_token}/subgraphs/id/H3XsUaJ4mTTP3qp2TEPkBY2oqr6ZcKVrfQu9aj8EMFGm"

# GraphQL query and variables
query = """
query($Account: String!) {
  positions(where: {account: $Account}) {
    market {
      name
      reserveToken {
        id
      }
    }
    account {
      id
    }
    snapshots {
      timestamp
      blockNumber
      netSupply
    }
  }
}
"""

variables = {
    "Account": account_id
}

# Make the HTTP POST request
response = requests.post(url, json={'query': query, 'variables': variables})
if response.status_code == 200:
    data = response.json()
    
    # Create or open the CSV file
    output_filename = f"{account_id}_positions.csv"
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write CSV Header
        writer.writerow(["Account ID", "Market Name", "Reserve Token ID", "Timestamp", "Block Number", "Net Supply"])

        # Process each position
        for position in data['data']['positions']:
            account = position['account']['id']
            market_name = position['market']['name']
            reserve_token_id = position['market']['reserveToken']['id']
            
            # Each snapshot can have multiple entries
            for snapshot in position['snapshots']:
                timestamp = snapshot['timestamp']
                block_number = snapshot['blockNumber']
                net_supply = snapshot['netSupply']
                writer.writerow([account, market_name, reserve_token_id, timestamp, block_number, net_supply])

    print(f"Data has been written to {output_filename}")
else:
    print(f"Failed to fetch data: {response.status_code}, {response.text}")
