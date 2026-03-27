// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts-upgradeable/governance/GovernorUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/governance/GovernorSettingsUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/governance/GovernorCountingSimpleUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/governance/GovernorVotesUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/governance/GovernorVotesQuorumFractionUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/governance/TimelockControllerUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

/**
 * @title UmbaneGovernor
 * @dev DAO governance for Umbane carbon token (aC) holders
 * 
 * DESIGN (see docs/umbane_dao_governance_analysis.md):
 * - Phase 1: Multi-sig council (Gnosis Safe) - contract not needed yet
 * - Phase 2: OpenZeppelin Governor with hybrid governance
 * - Phase 3: Full DAO (after 18 months)
 * 
 * This contract implements Phase 2 - Hybrid Governance:
 * - Voting token: aC (carbon credits)
 * - Voting delay: 2 days
 * - Voting period: 5 days  
 * - Quorum: 4% of total aC supply
 * - Multi-sig can veto for first 12 months
 */
contract UmbaneGovernor is 
    Initializable,
    GovernorUpgradeable,
    GovernorSettingsUpgradeable,
    GovernorCountingSimpleUpgradeable,
    GovernorVotesUpgradeable,
    GovernorVotesQuorumFractionUpgradeable,
    OwnableUpgradeable,
    UUPSUpgradeable 
{
    
    /// @notice Multi-sig address that can veto proposals (Phase 2 only)
    address public councilMultiSig;
    
    /// @notice Whether the council veto is active
    bool public councilVetoActive;
    
    /// @notice Timestamp when veto expires (12 months from Phase 2 start)
    uint256 public vetoExpiry;
    
    /// @notice Minimum aC tokens required to create a proposal
    uint256 public proposalThreshold;
    
    /// @notice Maximum voting power any single address can have
    uint256 public maxVotingPower;
    
    /// @notice Tracks if an address has voted (to prevent double voting)
    mapping(uint256 => mapping(address => bool)) public hasVoted;
    
    /// @notice Proposal veto status
    mapping(uint256 => bool) public proposalVetoed;
    
    /// @notice Emitted when a proposal is vetoed by council
    event ProposalVetoed(uint256 proposalId, address vetoer);
    
    /// @notice Emitted when council address is updated
    event CouncilUpdated(address oldCouncil, address newCouncil);
    
    /// @notice Emitted when veto is deactivated
    event VetoDeactivated();
    
    /**
     * @dev Constructor for upgradeable pattern
     */
    constructor() {
        _disableInitializers();
    }
    
    /**
     * @dev Initialize the governor
     * @param _token The voting token (aC - Umbane Carbon)
     * @param _timelock The timelock controller
     * @param _council Multi-sig address for veto power
     */
    function initialize(
        IVotesUpgradeable _token,
        TimelockControllerUpgradeable _timelock,
        address _council,
        uint256 _vetoDuration
    ) public initializer {
        __Governor_init("UmbaneGovernor");
        __GovernorSettings_init(
            2 days,    // votingDelay
            5 days,    // votingPeriod
            100e18     // proposalThreshold (100 aC)
        );
        __GovernorCountingSimple_init();
        __GovernorVotes_init(_token);
        __GovernorVotesQuorumFraction_init(4); // 4% quorum
        __Ownable_init(msg.sender);
        __UUPSUpgradeable_init();
        
        councilMultiSig = _council;
        councilVetoActive = true;
        vetoExpiry = block.timestamp + _vetoDuration; // 12 months
        maxVotingPower = 500e18; // Max 500 aC voting power per address (5% cap)
    }
    
    /**
     * @dev Override to set the name
     */
    function name() public pure override returns (string memory) {
        return "Umbane DAO";
    }
    
    /**
     * @dev Override to set the symbol
     */
    function symbol() public pure override returns (string memory) {
        return "UMB-GOV";
    }
    
    /**
     * @dev Override version for compatibility
     */
    function version() public pure override returns (string memory) {
        return "1.0.0";
    }
    
    /**
     * @dev Returns the voting weight for an account
     * @dev Implements max voting power cap to prevent whale dominance
     */
    function getVotes(address account, uint256 blockNumber) public view override returns (uint256) {
        uint256 votes = super.getVotes(account, blockNumber);
        // Cap voting power at maxVotingPower
        if (votes > maxVotingPower) {
            return maxVotingPower;
        }
        return votes;
    }
    
    /**
     * @dev Execute a proposal that has passed
     * @param proposalId The proposal ID
     * @param targetIds Array of target contract IDs
     * @param values Array of native token values
     * @param calldatas Array of encoded function calls
     * @param descriptionHash Hash of the proposal description
     */
    function execute(
        uint256[] memory targetIds,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) public payable override returns (uint256) {
        // Check if proposal was vetoed
        uint256 proposalId = hashProposal(targetIds, values, calldatas, descriptionHash);
        require(!proposalVetoed[proposalId], "Proposal was vetoed");
        
        return super.execute(targetIds, values, calldatas, descriptionHash);
    }
    
    /**
     * @dev Council can veto a proposal before it executes
     * @param proposalId The proposal ID to veto
     */
    function councilVeto(uint256 proposalId) external {
        require(msg.sender == councilMultiSig, "Only council can veto");
        require(councilVetoActive, "Veto not active");
        require(block.timestamp < vetoExpiry, "Veto period expired");
        
        proposalVetoed[proposalId] = true;
        emit ProposalVetoed(proposalId, msg.sender);
    }
    
    /**
     * @dev Deactivate the council veto (Phase 3)
     * @dev Can only be called after vetoExpiry
     */
    function deactivateVeto() external onlyOwner {
        require(block.timestamp >= vetoExpiry, "Veto not yet expired");
        require(councilVetoActive, "Veto already inactive");
        
        councilVetoActive = false;
        emit VetoDeactivated();
    }
    
    /**
     * @dev Update the council multi-sig address
     * @param newCouncil New council address
     */
    function setCouncil(address newCouncil) external onlyOwner {
        address oldCouncil = councilMultiSig;
        councilMultiSig = newCouncil;
        emit CouncilUpdated(oldCouncil, newCouncil);
    }
    
    /**
     * @dev Override to add custom proposal validation
     */
    function propose(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        string memory description
    ) public override returns (uint256) {
        // Check proposal threshold
        require(
            getVotes(msg.sender, block.number) >= proposalThreshold,
            "Below proposal threshold"
        );
        
        return super.propose(targets, values, calldatas, description);
    }
    
    /**
     * @dev Override to track voter participation
     */
    function _castVote(
        uint256 proposalId,
        address account,
        uint8 support,
        bytes memory reason
    ) internal override returns (uint256) {
        uint256 weight = super._castVote(proposalId, account, support, reason);
        hasVoted[proposalId][account] = true;
        return weight;
    }
    
    /**
     * @dev Returns true if the contract supports interface
     */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(GovernorUpgradeable, ERC165Upgradeable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
    
    /**
     * @dev UUPS upgrade authorization
     */
    function _authorizeUpgrade(address newImplementation)
        internal
        override
        onlyOwner
    {}
}

// ============================================
// TIMELOCK CONTRACT (needed for Governor)
// ============================================

/**
 * @title UmbaneTimelock
 * @dev Timelock controller for proposal execution
 * 
 * Provides a delay between proposal passage and execution,
 * allowing users to exit positions if they disagree.
 */
contract UmbaneTimelock is TimelockControllerUpgradeable {
    
    /// @notice Minimum delay between proposal passing and execution
    uint256 public constant MIN_DELAY = 2 days;
    
    /// @notice Maximum delay (governance parameter)
    uint256 public constant MAX_DELAY = 30 days;
    
    /**
     * @dev Initialize the timelock
     * @param _minDelay Minimum delay for proposals
     * @param _proposers Accounts that can propose
     * @param _executors Accounts that can execute
     * @param _admin Optional admin (usually the Governor)
     */
    function initialize(
        uint256 _minDelay,
        address[] memory _proposers,
        address[] memory _executors,
        address _admin
    ) public initializer {
        // 2 days minimum delay
        require(_minDelay >= MIN_DELAY, "Min delay too low");
        
        __TimelockController_init(_minDelay, _proposers, _executors, _admin);
    }
}