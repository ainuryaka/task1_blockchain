// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract TaskBlockchainNFT is ERC721URIStorage, Ownable {
    uint256 public mintPrice;
    uint256 public totalSupply;
    uint256 public maxSupply;
    uint256 public maxPerWallet;
    bool public isPublicMintEnabled;
    string public baseTokenUri;
    address payable public withdrawWallet;
    mapping(address => uint256) public walletMints;

    constructor() payable ERC721("TaskBlockchain", "RP") {
        mintPrice = 0.015 ether;
        totalSupply = 0;
        maxSupply = 1000;
        maxPerWallet = 3;
    }

    function setIsPublicMintEnabled(bool isPublicMintEnabled_arg) external onlyOwner {
        isPublicMintEnabled = isPublicMintEnabled_arg;
    }

    function setBaseTokenUri(string calldata baseTokenUri_arg) external onlyOwner {
        baseTokenUri = baseTokenUri_arg;
    }

    function tokenURI(uint256 tokenId_) public view override returns (string memory) {
        require(_exists(tokenId_), "Token does not exist");
        return string(abi.encodePacked(baseTokenUri, Strings.toString(tokenId_), ".json"));
    }


    function withdraw() external onlyOwner {
        require(address(this).balance > 0, "No balance to withdraw");
        (bool success, ) = withdrawWallet.call{ value: address(this).balance }("");
        require(success, "Withdrawal failed, try again");
    }

    function mint(uint256 quantity_arg) public payable {
        require(isPublicMintEnabled, "Minting is disabled, try again");
        require(msg.value == quantity_arg * mintPrice, "Incorrect mint value");
        require(totalSupply + quantity_arg <= maxSupply, "Sold out, wait until next time");
        require(walletMints[msg.sender] + quantity_arg <= maxPerWallet, "Exceeds max wallet limit");

        for (uint256 i = 0; i < quantity_arg; i++) {
            uint256 newTokenId = totalSupply + 1;
            totalSupply++;
            _safeMint(msg.sender, newTokenId);
        }
    }
}
