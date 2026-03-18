// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "../contracts/Token.sol";

contract InitializeToken is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        Token token = Token(payable(0xa4817F92897Dc9BD0302b465445C242b3Da0Af3c));
        token.initialize();

        console.log("Token initialized at:", address(token));
        console.log("Owner:", token.owner());

        vm.stopBroadcast();
    }
}
