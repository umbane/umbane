// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Token is ERC20 {
    constructor() ERC20("MyToken", "MTK") {}

    uint256 public mJTotalSupply;
    uint256 public aCTotalSupply;

    function mintMJ(address to, uint256 amount) public {
        _mint(to, amount);
        mJTotalSupply += amount;
    }

    function mintAC(address to, uint256 amount) public {
        _mint(to, amount);
        aCTotalSupply += amount;
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
}
