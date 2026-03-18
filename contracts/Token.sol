// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Token is ERC20, VRFConsumerBaseV2 {
    constructor() ERC20("UmbaneToken", "UMB") VRFConsumerBaseV2(0x2Ca8E0C643bDe4C2D8c8B8B77586A8EDd60178B9) {}

    uint256 public mJTotalSupply;
    uint256 public aCTotalSupply;

    event MJMinted(address indexed to, uint256 amount);
    event ACMinted(address indexed to, uint256 amount);
    event RequestEnergyData(bytes32 indexed requestId, address indexed user);
    event CarbonPriceUpdated(int256 price);

    uint64 public s_subscriptionId;
    bytes32 public keyHash;
    uint32 public callbackGasLimit;
    uint16 public requestConfirmations;
    uint32 public numWords;
    LinkTokenInterface internal linkToken;

    AggregatorV3Interface internal carbonPriceFeed;
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

    function setChainlinkConfig(
        uint64 subscriptionId,
        bytes32 _keyHash,
        uint32 _callbackGasLimit,
        uint16 _requestConfirmations,
        uint32 _numWords,
        address _linkToken
    ) public {
        s_subscriptionId = subscriptionId;
        keyHash = _keyHash;
        callbackGasLimit = _callbackGasLimit;
        requestConfirmations = _requestConfirmations;
        numWords = _numWords;
        linkToken = LinkTokenInterface(_linkToken);
    }

    function setCarbonPriceFeed(address _feedAddress) external {
        carbonPriceFeed = AggregatorV3Interface(_feedAddress);
    }

    function updateCarbonPrice() external {
        require(address(carbonPriceFeed) != address(0), "Carbon feed not set");
        (
            /*uint80 roundID*/,
            int256 answer,
            /*uint256 startedAt*/,
            uint256 updatedAt,
            /*uint80 answeredInRound*/
        ) = carbonPriceFeed.latestRoundData();
        require(answer > 0, "Invalid price");
        latestCarbonPrice = answer;
        latestCarbonPriceTimestamp = updatedAt;
        emit CarbonPriceUpdated(answer);
    }

    function getCarbonPrice() external view returns (int256, uint256) {
        return (latestCarbonPrice, latestCarbonPriceTimestamp);
    }

    function calculateCarbonCredits(uint256 energyKWh) external pure returns (uint256) {
        uint256 co2Kg = energyKWh * 500 / 1000;
        return co2Kg * CARBON_CREDIT_KG_FACTOR;
    }

    function getCarbonValueUSD(uint256 acAmount) external view returns (int256) {
        require(latestCarbonPrice > 0, "Carbon price not set");
        return int256(acAmount) * latestCarbonPrice / int256(CARBON_CREDIT_KG_FACTOR);
    }

    function requestEnergyData(address user) public returns (bytes32 requestId) {
        requestId = requestRandomness(keyHash, requestConfirmations, callbackGasLimit, numWords);
        emit RequestEnergyData(requestId, user);
    }

    function fulfillRandomWords(uint256 requestId, uint256[] memory randomWords) internal override {
        uint256 energyUsed = randomWords[0] % 1000;
        address user = msg.sender;
        
        userEnergyHistory[user].push(UserEnergyRecord({
            periodStart: block.timestamp,
            energyUsed: energyUsed,
            processed: false
        }));
        
        uint256 carbonCredits = calculateCarbonCredits(energyUsed);
        pendingCarbonCredits[user] += carbonCredits;
        
        mintMJ(user, energyUsed);
    }

    function processEnergyRecord(address user) external {
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

    function mintMJ(address to, uint256 amount) public {
        _mint(to, amount);
        mJTotalSupply += amount;
        emit MJMinted(to, amount);
    }

    function mintAC(address to, uint256 amount) public {
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
