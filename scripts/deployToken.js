const hre = require("hardhat");

async function main() {
  const AdacToken = await hre.ethers.getContractFactory("AdacToken");
  const token = await AdacToken.deploy();

  await token.waitForDeployment();

  console.log(`ADAC Token deployed to ${token.target}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});