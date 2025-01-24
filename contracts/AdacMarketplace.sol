// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import {AdacToken} from "./AdacToken.sol";

contract AdacMarketplace is ReentrancyGuard {
    using Counters for Counters.Counter;
    
    AdacToken public adacToken;
    Counters.Counter private _listingIds;
    uint256 public listingFee = 0.025 ether;

    struct Listing {
        uint256 listingId;
        address nftContract;
        uint256 tokenId;
        address payable seller;
        uint256 price;
        bool active;
    }

    mapping(uint256 => Listing) public listings;
    
    event Listed(
        uint256 indexed listingId,
        address indexed nftContract,
        uint256 indexed tokenId,
        address seller,
        uint256 price
    );
    
    event Sale(
        uint256 indexed listingId,
        address indexed nftContract,
        uint256 indexed tokenId,
        address seller,
        address buyer,
        uint256 price
    );

    constructor(address _adacToken) {
        adacToken = AdacToken(_adacToken);
    }

    function listNFT(
        address nftContract,
        uint256 tokenId,
        uint256 price
    ) external payable nonReentrant {
        require(msg.value == listingFee, "Must pay listing fee");
        require(price > 0, "Price must be greater than 0");
        require(
            IERC721(nftContract).getApproved(tokenId) == address(this),
            "NFT not approved for marketplace"
        );

        _listingIds.increment();
        uint256 listingId = _listingIds.current();

        listings[listingId] = Listing(
            listingId,
            nftContract,
            tokenId,
            payable(msg.sender),
            price,
            true
        );

        emit Listed(listingId, nftContract, tokenId, msg.sender, price);
    }

    function buyNFT(uint256 listingId) external nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.active, "Listing not active");
        
        require(
            adacToken.transferFrom(msg.sender, listing.seller, listing.price),
            "Token transfer failed"
        );

        IERC721(listing.nftContract).safeTransferFrom(
            listing.seller,
            msg.sender,
            listing.tokenId
        );

        listing.active = false;

        emit Sale(
            listingId,
            listing.nftContract,
            listing.tokenId,
            listing.seller,
            msg.sender,
            listing.price
        );
    }

    function cancelListing(uint256 listingId) external nonReentrant {
        Listing storage listing = listings[listingId];
        require(msg.sender == listing.seller, "Not the seller");
        require(listing.active, "Listing not active");
        
        listing.active = false;
        payable(msg.sender).transfer(listingFee);
    }

    function getListings() external view returns (Listing[] memory) {
        uint256 totalListings = _listingIds.current();
        uint256 activeCount = 0;
        
        for (uint256 i = 1; i <= totalListings; i++) {
            if (listings[i].active) {
                activeCount++;
            }
        }

        Listing[] memory activeListings = new Listing[](activeCount);
        uint256 currentIndex = 0;

        for (uint256 i = 1; i <= totalListings; i++) {
            if (listings[i].active) {
                activeListings[currentIndex] = listings[i];
                currentIndex++;
            }
        }

        return activeListings;
    }
}