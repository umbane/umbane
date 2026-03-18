
# One liners

## Deploy a contract
cd /home/ubuntupunk/Projects/umbane && source /dev/stdin <<< "$(cat .env | grep -v '^#' | grep '=' | sed 's/^/export /')" && forge script script/Deploy.s.sol --rpc-url polygon_amoy --broadcast --gas-limit 5000000 2>&1 | tail -20
