pragma solidity ^0.5.3;


import "./ERC20.sol";

contract WonderfulERC20 is ERC20 {

    function getWonderfulMessage() public pure returns(string memory) {
        return "Wonderful message";
    }
    
}