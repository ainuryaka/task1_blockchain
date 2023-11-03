from web3 import Web3, HTTPProvider
from solcx import compile_source

w3 = Web3(HTTPProvider("http://localhost:8545"))  # Connect to your Ethereum node

# Compile the contract
contract_source = """
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721, Ownable {
    constructor() ERC721("MyNFT", "NFT") {}

    function mintNFT(address to) public onlyOwner {
        uint256 tokenId = totalSupply();
        _mint(to, tokenId);
    }
}
"""

compiled_contract = compile_source(contract_source)
contract_interface = compiled_contract["<stdin>:MyNFT"]

# Deploy the contract
contract = w3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface["bin"])
tx_hash = contract.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Write the test
def test_mint_nfts():
    contract_instance = w3.eth.contract(
        address=tx_receipt.contractAddress, abi=contract_interface["abi"]
    )

    owner = w3.eth.accounts[0]

    # Mint NFTs
    num_minted = 5
    for i in range(num_minted):
        contract_instance.functions.mintNFT(owner).transact()

    # Check the total supply
    total_supply = contract_instance.functions.totalSupply().call()
    assert total_supply == num_minted


def test_assign_ownership():
    contract_instance = w3.eth.contract(
        address=tx_receipt.contractAddress, abi=contract_interface["abi"]
    )

    owner = w3.eth.accounts[0]

    # Mint an NFT
    contract_instance.functions.mintNFT(owner).transact()

    # Check the owner of the NFT
    owner_of_nft = contract_instance.functions.ownerOf(0).call()
    assert owner_of_nft == owner


def test_transfer_nfts():
    contract_instance = w3.eth.contract(
        address=tx_receipt.contractAddress, abi=contract_interface["abi"]
    )

    owner = w3.eth.accounts[0]
    new_owner = w3.eth.accounts[1]

    # Mint an NFT
    contract_instance.functions.mintNFT(owner).transact()

    # Transfer the NFT from the owner to a new owner
    contract_instance.functions.transferFrom(owner, new_owner, 0).transact()

    # Check the new owner of the NFT
    owner_of_nft = contract_instance.functions.ownerOf(0).call()
    assert owner_of_nft == new_owner
