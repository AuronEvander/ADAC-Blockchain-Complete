const { expect } = require("chai");

describe("AdacGovernance", function () {
  let token;
  let governance;
  let owner;
  let proposer;
  let voter1;
  let voter2;

  beforeEach(async function () {
    [owner, proposer, voter1, voter2] = await ethers.getSigners();
    
    const Token = await ethers.getContractFactory("AdacToken");
    token = await Token.deploy();
    
    const Governance = await ethers.getContractFactory("AdacGovernance");
    governance = await Governance.deploy(await token.getAddress());

    // Give tokens to proposer and voters
    await token.mint(proposer.address, ethers.parseEther("200000")); // 200k tokens
    await token.mint(voter1.address, ethers.parseEther("50000")); // 50k tokens
    await token.mint(voter2.address, ethers.parseEther("50000")); // 50k tokens
  });

  describe("Proposal Creation", function () {
    it("Should allow proposal creation with enough tokens", async function () {
      await governance.connect(proposer).propose("Test Proposal");
      expect(await governance.proposalCount()).to.equal(1);
    });

    it("Should fail if proposer has insufficient tokens", async function () {
      await expect(
        governance.connect(voter1).propose("Test Proposal")
      ).to.be.revertedWith("AdacGovernance: insufficient balance to propose");
    });
  });

  describe("Voting", function () {
    beforeEach(async function () {
      await governance.connect(proposer).propose("Test Proposal");
    });

    it("Should allow voting", async function () {
      await governance.connect(voter1).castVote(1, true);
      const proposal = await governance.getProposal(1);
      expect(proposal.forVotes).to.equal(ethers.parseEther("50000"));
    });

    it("Should prevent double voting", async function () {
      await governance.connect(voter1).castVote(1, true);
      await expect(
        governance.connect(voter1).castVote(1, true)
      ).to.be.revertedWith("AdacGovernance: already voted");
    });
  });

  describe("Execution", function () {
    beforeEach(async function () {
      await governance.connect(proposer).propose("Test Proposal");
    });

    it("Should not allow execution before voting period ends", async function () {
      await expect(
        governance.execute(1)
      ).to.be.revertedWith("AdacGovernance: voting is still open");
    });

    it("Should allow execution after voting period", async function () {
      await ethers.provider.send("evm_increaseTime", [3 * 24 * 60 * 60 + 1]); // 3 days + 1 second
      await governance.execute(1);
      const proposal = await governance.getProposal(1);
      expect(proposal.executed).to.be.true;
    });
  });
});