// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract fairbetToken is ERC20 {

    uint256 public initialBalance = 500 * 10 ** decimals(); // 500 tokens with decimals considered
    mapping(address => bool) public hasClaimedTokens;  // To track if the user has received initial tokens
   
    constructor() ERC20("Fairbet Token", "FB") {  // Name: "CustomToken", Symbol: "CTK"
        _mint(msg.sender, 1000000 * 10 ** decimals()); // Mint 1,000,000 tokens to the contract owner
    }

    // Function to fund the user with 500 tokens when they log in (i.e., connect their wallet)
    function fundUser() external {
        if(hasClaimedTokens[msg.sender]){
            revert("User has already claimed tokens");
        }
        _mint(msg.sender, initialBalance);
        hasClaimedTokens[msg.sender] = true;
    }

    // Standard transfer function
    function transferTokens( address recipient, uint256 amount) external returns (bool) {
        _transfer(msg.sender, recipient, amount*10 ** decimals());
        return true;
    } 

    function victorySend(uint256 amount) external returns (bool) {
        _transfer( 0x56375D354043571d89bfcAeec1Ba0949007c529A , msg.sender, amount*10**decimals());
        return true;
    }
}
