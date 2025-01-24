const { expect } = require("chai");

describe("AdacMarketplace", function () {
  let Token;
  let token;
  let Marketplace;
  let marketplace;
  let owner;
  let seller;
  let buyer;
  let nftContract;

  beforeEach(async function () {
    [owner, seller, buyer, nftContract] = await ethers.getSigners();
    
    Token = await ethers.getContractFactory("AdacToken");
    token = await Token.deploy();
    
    Marketplace = await ethers.getContractFactory("AdacMarketplace");
    marketplace = await Marketplace.deploy(await token.getAddress());
  });

  describe("Listing", function () {
    const listingFee = ethers.parseEther("0.025");
    const tokenId = 1;
    const price = 100;

    it("Should create a listing", async function () {
      await marketplace.connect(seller).listNFT(nftContract.address, tokenId, price, { value: listingFee });
      
      const listings = await marketplace.getListings();
      expect(listings.length).to.equal(1);
      expect(listings[0].seller).to.equal(seller.address);
      expect(listings[0].price).to.equal(price);
    });

    it("Should fail without listing fee", async function () {
      await expect(
        marketplace.connect(seller).listNFT(nftContract.address, tokenId, price)
      ).to.be.revertedWith("Must pay listing fee");
    });
  });

  describe("Buying", function () {
    const listingFee = ethers.parseEther("0.025");
    const tokenId = 1;
    const price = 100;

    beforeEach(async function () {
      await marketplace.connect(seller).listNFT(nftContract.address, tokenId, price, { value: listingFee });
      await token.mint(buyer.address, price * 2);
      await token.connect(buyer).approve(marketplace.getAddress(), price);
    });

    it("Should allow token purchase", async function () {
      const initialSellerBalance = await token.balanceOf(seller.address);
      
      await marketplace.connect(buyer).buyNFT(1);
      
      expect(await token.balanceOf(seller.address)).to.equal(initialSellerBalance + BigInt(price));
    });

    it("Should fail if listing is not active", async function () {
      await marketplace.connect(buyer).buyNFT(1);
      await expect(
        marketplace.connect(buyer).buyNFT(1)
      ).to.be.revertedWith("Listing not active");
    });
  });

  describe("Cancel Listing", function () {
    const listingFee = ethers.parseEther("0.025");
    const tokenId = 1;
    const price = 100;

    beforeEach(async function () {
      await marketplace.connect(seller).listNFT(nftContract.address, tokenId, price, { value: listingFee });
    });

    it("Should allow seller to cancel listing", async function () {
      await marketplace.connect(seller).cancelListing(1);
      const listings = await marketplace.getListings();
      expect(listings.length).to.equal(0);
    });

    it("Should fail if non-seller tries to cancel", async function () {
      await expect(
        marketplace.connect(buyer).cancelListing(1)
      ).to.be.revertedWith("Not the seller");
    });
  });
});