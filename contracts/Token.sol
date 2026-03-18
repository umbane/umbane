// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract Token is Initializable, ERC20Upgradeable, OwnableUpgradeable {
    
    uint256 public mJTotalSupply;
    uint256 public aCTotalSupply;

    event MJMinted(address indexed to, uint256 amount);
    event ACMinted(address indexed to, uint256 amount);
    event CarbonPriceUpdated(int256 price);

    int256 public latestCarbonPrice;
    uint256 public latestCarbonPriceTimestamp;

    uint256 public constant CARBON_CREDIT_KG_FACTOR = 1000;

    struct UserEnergyRecord {
        uint256 periodStart;
        uint256 energyUsed;
        bool processed;
    }
    mapping(address => UserEnergyRecord[]) public userEnergyHistory;
    mapping(address => uint256) public pendingCarbonCredits;

    constructor() {}

    function initialize() public initializer {
        __ERC20_init("Umbane", "UMBANE");
        __Ownable_init(msg.sender);
    }

    function setCarbonPrice(int256 _price) external onlyOwner {
        require(_price > 0, "Invalid price");
        latestCarbonPrice = _price;
        latestCarbonPriceTimestamp = block.timestamp;
        emit CarbonPriceUpdated(_price);
    }

    function getCarbonPrice() external view returns (int256, uint256) {
        return (latestCarbonPrice, latestCarbonPriceTimestamp);
    }

    function calculateCarbonCredits(uint256 energyKWh) internal pure returns (uint256) {
        uint256 co2Kg = energyKWh * 500 / 1000;
        return co2Kg * CARBON_CREDIT_KG_FACTOR;
    }

    function getCarbonValueUSD(uint256 acAmount) external view returns (int256) {
        require(latestCarbonPrice > 0, "Carbon price not set");
        return int256(acAmount) * latestCarbonPrice / int256(CARBON_CREDIT_KG_FACTOR);
    }

    function recordEnergyUsage(address user, uint256 energyUsed) external onlyOwner {
        userEnergyHistory[user].push(UserEnergyRecord({
            periodStart: block.timestamp,
            energyUsed: energyUsed,
            processed: false
        }));
        
        uint256 carbonCredits = calculateCarbonCredits(energyUsed);
        pendingCarbonCredits[user] += carbonCredits;
        
        mintMJ(user, energyUsed);
    }

    function processEnergyRecord(address user) external onlyOwner {
        UserEnergyRecord[] storage records = userEnergyHistory[user];
        uint256 pending = pendingCarbonCredits[user];
        
        for (uint256 i = 0; i < records.length; i++) {
            if (!records[i].processed) {
                records[i].processed = true;
            }
        }
        
        if (pending > 0) {
            pendingCarbonCredits[user] = 0;
            mintAC(user, pending);
        }
    }

    function mintMJ(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
        mJTotalSupply += amount;
        emit MJMinted(to, amount);
    }

    function mintAC(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
        aCTotalSupply += amount;
        emit ACMinted(to, amount);
    }

    function burnMJ(uint256 amount) public {
        _burn(msg.sender, amount);
        mJTotalSupply -= amount;
    }

    function burnAC(uint256 amount) public {
        _burn(msg.sender, amount);
        aCTotalSupply -= amount;
    }

    function getMJBalance(address account) public view returns (uint256) {
        return balanceOf(account);
    }

    function getACBalance(address account) public view returns (uint256) {
        return balanceOf(account);
    }

    function getUserPendingCredits(address user) external view returns (uint256) {
        return pendingCarbonCredits[user];
    }

    function getUserEnergyHistory(address user) external view returns (UserEnergyRecord[] memory) {
        return userEnergyHistory[user];
    }
}
