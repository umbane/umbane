from web3 import Web3
import os

w3 = Web3(
    Web3.HTTPProvider(
        os.environ.get("POLYGON_PROVIDER_URL")
        or os.environ.get("POLYGON_AMOY_RPC_URL")
        or "https://rpc.ankr.com/polygon_amoy/d06f5dee9abc00217a93067745b34f68bae7d0349a74556a00450163c96615a4"
    )
)

contract_address = os.environ.get(
    "CONTRACT_ADDRESS", "0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe"
)

contract_abi = [
    {
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "amount", "type": "uint256"},
        ],
        "name": "mintMJ",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "amount", "type": "uint256"},
        ],
        "name": "mintAC",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "amount", "type": "uint256"},
        ],
        "name": "burnMJ",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "amount", "type": "uint256"},
        ],
        "name": "burnAC",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "user", "type": "address"},
            {"name": "energyUsed", "type": "uint256"},
        ],
        "name": "recordEnergyUsage",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "user", "type": "address"},
        ],
        "name": "processEnergyRecord",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"name": "_feedAddress", "type": "address"}],
        "name": "setCarbonPriceFeed",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [],
        "name": "updateCarbonPrice",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getCarbonPrice",
        "outputs": [
            {"name": "", "type": "int256"},
            {"name": "", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"name": "energyKWh", "type": "uint256"}],
        "name": "calculateCarbonCredits",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "pure",
        "type": "function",
    },
    {
        "inputs": [{"name": "acAmount", "type": "uint256"}],
        "name": "getCarbonValueUSD",
        "outputs": [{"name": "", "type": "int256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getUserPendingCredits",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

account_address = os.environ.get(
    "ACCOUNT_ADDRESS", "0x5Ee264d83332Ba0Cf46f8b1EB7B064e34d62d7Dc"
)
account_private_key = os.environ.get("ACCOUNT_PRIVATE_KEY", "")
