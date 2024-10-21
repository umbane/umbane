# Carbon Credits Smart Contract Documentation

This document outlines the relationships between the three Solidity smart contracts: `carboncredits.sol`, `credittoken.sol`, and `certification.sol`.

## Contract Relationships

* **`carboncredits.sol`:** This contract manages the registration of carbon credit holders, verifiers, and customers. It holds the core data about these entities, including their names, IDs, and associated addresses.

* **`credittoken.sol`:** This contract inherits from both `carboncredits.sol` and OpenZeppelin's ERC20 contract. It manages the creation, transfer, and burning of carbon credits as ERC20 tokens.  It interacts with `carboncredits.sol` to access and modify data about credit holders and verifiers.  Key functionalities include minting new tokens, transferring credits between accounts, and burning tokens.

* **`certification.sol`:** This contract inherits from `credittoken.sol`. It represents a specific certification standard (Gold Standard in this example) and adds functionality related to certification and minting of certified carbon credits. It uses functions from `credittoken.sol` to manage the tokens and interacts with the underlying data structures in `carboncredits.sol`.

## Overall Architecture

The contracts work together in a layered architecture:

1. **Data Management (`carboncredits.sol`):**  Provides the core data structures and functions for managing participants in the carbon credit system.

2. **Tokenization (`credittoken.sol`):**  Implements the ERC20 token standard to represent and manage carbon credits as fungible tokens.  It relies on the data in `carboncredits.sol`.

3. **Certification (`certification.sol`):**  Adds a layer of certification-specific logic, building upon the tokenization functionality in `credittoken.sol` and using the data from `carboncredits.sol`.


This layered approach allows for modularity and extensibility.  Future versions could add more certification standards or other features by creating new contracts that inherit from existing ones.
