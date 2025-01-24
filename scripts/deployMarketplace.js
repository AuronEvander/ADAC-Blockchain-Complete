const hre = require("hardhat");

async function main() {
  // Deploy token first
  const AdacToken = await hre.ethers.getContractFactory("AdacToken");
  const token = await AdacToken.deploy();
  await token.waitForDeployment();
  console.log(`ADAC Token deployed to ${token.target}`);

  // Deploy marketplace
  const AdacMarketplace = await hre.ethers.getContractFactory("AdacMarketplace");
  const marketplace = await AdacMarketplace.deploy(token.target);
  await marketplace.waitForDeployment();
  console.log(`ADAC Marketplace deployed to ${marketplace.target}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});