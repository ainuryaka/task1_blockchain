const hre = require("hardhat");

async function main() {
  const currentTimestampInSeconds = Math.round(Date.now() / 1000);
  const unlockTime = currentTimestampInSeconds + 60;

  const TaskBlockchainNFT = await hre.ethers.getContractFactory("TaskBlockchainNFT");
  const taskBlockchainNFT = await TaskBlockchainNFT.deploy();

  // Wait for the contract to be mined and get the receipt
  await taskBlockchainNFT.deployed();
  console.log("TaskBlockchainNFT deployed to address:", taskBlockchainNFT.address);

  const lockFactory = await hre.ethers.getContractFactory("Lock");
  const lock = await lockFactory.deploy(unlockTime, {
    value: hre.ethers.utils.parseEther("0.001"),
  });

  // Wait for the lock contract to be mined and get the receipt
  await lock.deployed();
  console.log("Lock deployed to address:", lock.address);

  console.log(
    `Lock with ${hre.ethers.utils.formatEther(hre.ethers.utils.parseEther("0.001"))} TaskBlockchainNFT and unlock timestamp ${unlockTime} deployed to ${lock.address}`
  );
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
