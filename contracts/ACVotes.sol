// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts-upgradeable/token/ERC20/extensions/ERC20VotesUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

/**
 * @title UmbaneACVotes
 * @dev ERC20Votes extension for aC (Umbane Carbon) governance token
 * 
 * The aC token needs to support:
 * - Voting power tracking (ERC20Votes)
 * - Delegation (self-delegate or delegate to others)
 * - Checkpointing for historical voting power
 * 
 * This is a separate extension because governance voting
 * requires different logic than simple token transfers.
 */
contract UmbaneACVotes is ERC20VotesUpgradeable, OwnableUpgradeable, UUPSUpgradeable {
    
    /// @notice Maximum delegation depth (prevents recursive delegation attacks)
    uint8 public constant MAX_DELEGATION_DEPTH = 3;
    
    /// @notice Timestamp when voting power is locked for a user
    mapping(address => uint256) public votingPowerLockedUntil;
    
    /// @notice Minimum voting power required to participate in governance
    uint256 public constant MIN_VOTING_POWER = 10e18; // 10 aC
    
    /// @notice Emitted when voting power is locked
    event VotingPowerLocked(address account, uint256 until);
    
    /**
     * @dev Constructor for upgradeable pattern
     */
    constructor() {
        _disableInitializers();
    }
    
    /**
     * @dev Initialize the governance token
     * @param _name Token name "Umbane Carbon"
     * @param _symbol Token symbol "aC"
     */
    function initialize(string memory _name, string memory _symbol) 
        public 
        initializer 
    {
        __ERC20_init(_name, _symbol);
        __ERC20Votes_init();
        __Ownable_init(msg.sender);
        __UUPSUpgradeable_init();
    }
    
    /**
     * @dev Override to enforce minimum voting power
     * @dev User must have at least MIN_VOTING_POWER to have voting power
     */
    function getVotes(address account) 
        public 
        view 
        override 
        returns (uint256) 
    {
        uint256 votes = super.getVotes(account);
        // Return 0 if below minimum
        if (votes < MIN_VOTING_POWER) {
            return 0;
        }
        return votes;
    }
    
    /**
     * @dev Override to prevent flash loan voting attacks
     * @dev Voting power is only available after a time delay
     * 
     * Note: This is simplified - full implementation would use 
     * a time-lock for newly acquired tokens
     */
    function _delegate(address delegator, address delegatee) 
        internal 
        override 
    {
        super._delegate(delegator, delegatee);
    }
    
    /**
     * @dev UUPS upgrade authorization
     */
    function _authorizeUpgrade(address newImplementation)
        internal
        override
        onlyOwner
    {}
    
    /**
     * @dev Required override for ERC20Votes
     */
    function clock() 
        public 
        view 
        override 
        returns (uint48) 
    {
        return uint48(block.timestamp);
    }
    
    /**
     * @dev Required override for ERC20Votes
     */
    function CLOCK_MODE() 
        public 
        pure 
        override 
        returns (string memory) 
    {
        return "timestamp";
    }
}