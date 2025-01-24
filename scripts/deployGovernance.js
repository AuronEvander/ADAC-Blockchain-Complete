const hre = require("hardhat");

async function main() {
  // Deploy token first
  const AdacToken = await hre.ethers.getContractFactory("AdacToken");
  const token = await AdacToken.deploy();
  await token.waitForDeployment();
  console.log(`ADAC Token deployed to ${token.target}`);

  // Deploy governance
  const AdacGovernance = await hre.ethers.getContractFactory("AdacGovernance");
  const governance = await AdacGovernance.deploy(token.target);
  await governance.waitForDeployment();
  console.log(`ADAC Governance deployed to ${governance.target}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});