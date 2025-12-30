# Carbon Credit Blockchain Integration

This project now includes real blockchain functionality using Web3.py and Solidity smart contracts for carbon credit management.

## 🏗️ Architecture

### Smart Contracts
- **CarbonCreditToken.sol**: ERC20 token for carbon credits with project tracking
- **CarbonCreditMarketplace.sol**: Marketplace for trading credits and managing tenders

### Backend Integration
- **Web3BlockchainManager**: Real blockchain integration using Web3.py
- **SimpleBlockchain**: Fallback in-memory blockchain for development
- **BlockchainService**: Service layer for blockchain operations
- **BlockchainConfig**: Django model for network configuration

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install contract dependencies
cd contracts
npm install
```

### 2. Setup Local Blockchain

```bash
# Start Hardhat local node
cd contracts
npx hardhat node
```

### 3. Deploy Contracts

```bash
# Deploy to local network
python scripts/deploy_contracts.py --network localhost

# Or use the management command to setup blockchain config first
python manage.py setup_blockchain --network local --generate-key
```

### 4. Run Django

```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

## 🔧 Configuration

### Blockchain Networks

The system supports multiple networks:

- **Local**: Hardhat local development network
- **Sepolia**: Ethereum testnet
- **Goerli**: Ethereum testnet (deprecated)
- **Mainnet**: Ethereum mainnet

### Environment Variables

Add to your `.env` file:

```env
# Blockchain Configuration
BLOCKCHAIN_NETWORK=local
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
BLOCKCHAIN_PRIVATE_KEY=your_private_key_here

# For testnets/mainnet
INFURA_PROJECT_ID=your_infura_project_id
ETHERSCAN_API_KEY=your_etherscan_api_key
```

## 📋 Management Commands

### Setup Blockchain Configuration

```bash
# Setup local development
python manage.py setup_blockchain --network local --generate-key

# Setup Sepolia testnet
python manage.py setup_blockchain --network sepolia --rpc-url https://sepolia.infura.io/v3/YOUR_PROJECT_ID

# Use existing private key
python manage.py setup_blockchain --network local --private-key 0x1234...
```

## 🔄 Blockchain Operations

### Project Registration
When a project is approved, it's automatically registered on the blockchain:

```python
from api.blockchain_service import BlockchainService

# Register project
tx_hash = BlockchainService.register_project_on_blockchain(project)
```

### Credit Minting
Approved projects get credits minted to the NGO's wallet:

```python
# Mint credits
tx_hash = BlockchainService.mint_credits_for_project(project)
```

### Credit Transfers
Credits can be transferred between users:

```python
# Transfer credits
tx_hash = BlockchainService.transfer_credits(from_user, to_user, amount, project_id)
```

### Balance Queries
Get user's token balance:

```python
# Get balance
balance = BlockchainService.get_user_balance(user)
```

## 🎯 Smart Contract Features

### CarbonCreditToken (CCT)
- ERC20 compliant token
- Project-based credit tracking
- Minting controls (only owner)
- Pausable functionality
- Burnable tokens

### CarbonCreditMarketplace
- Tender creation and management
- Proposal submission system
- Direct credit listings
- Marketplace fees
- Automated escrow

## 🔐 Security Features

- Private key encryption
- Role-based access control
- Pausable contracts
- Reentrancy protection
- Gas optimization

## 🧪 Testing

### Local Development
```bash
# Start local blockchain
cd contracts
npx hardhat node

# Deploy contracts
python scripts/deploy_contracts.py --network localhost

# Test in Django shell
python manage.py shell
>>> from api.blockchain_service import BlockchainService
>>> status = BlockchainService.get_blockchain_status()
>>> print(status)
```

### Contract Testing
```bash
cd contracts
npx hardhat test
```

## 📊 Admin Interface

The Django admin includes blockchain management:

1. **Blockchain Configs**: Manage network configurations
2. **Wallets**: View user wallets and balances
3. **Chain Blocks**: View blockchain blocks (for simple blockchain)
4. **Chain Transactions**: View all transactions

## 🔄 Migration from Simple Blockchain

The system automatically falls back to the simple blockchain if Web3 connection fails. To migrate:

1. Setup blockchain configuration
2. Deploy contracts
3. Existing data remains in the simple blockchain
4. New operations use real blockchain

## 🚨 Production Deployment

### Testnet Deployment (Sepolia)

```bash
# Setup configuration
python manage.py setup_blockchain --network sepolia --rpc-url https://sepolia.infura.io/v3/YOUR_PROJECT_ID

# Deploy contracts
python scripts/deploy_contracts.py --network sepolia
```

### Mainnet Deployment

⚠️ **Warning**: Mainnet deployment requires real ETH for gas fees.

```bash
# Setup configuration
python manage.py setup_blockchain --network mainnet --rpc-url https://mainnet.infura.io/v3/YOUR_PROJECT_ID

# Deploy contracts (ensure you have sufficient ETH)
python scripts/deploy_contracts.py --network mainnet
```

## 🔍 Monitoring

### Blockchain Status
Check connection status:

```python
from api.blockchain_service import BlockchainService
status = BlockchainService.get_blockchain_status()
```

### Transaction Monitoring
All blockchain transactions are logged in `ChainTransaction` model with:
- Transaction hash
- Block number
- Gas used
- Metadata

## 🛠️ Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check RPC URL
   - Verify network is running
   - Check firewall settings

2. **Transaction Failed**
   - Insufficient gas
   - Invalid parameters
   - Contract not deployed

3. **Private Key Issues**
   - Ensure key has 0x prefix
   - Check key format (64 hex characters)
   - Verify account has ETH for gas

### Logs
Check Django logs for blockchain operations:

```bash
tail -f logs/django.log | grep blockchain
```

## 📚 API Integration

The blockchain functionality integrates seamlessly with existing API endpoints:

- Project approval automatically triggers credit minting
- Purchase transactions create blockchain transfers
- Tender system uses smart contract marketplace
- User balances reflect real token holdings

## 🔮 Future Enhancements

- Multi-signature wallets
- Staking mechanisms
- Carbon offset verification
- Cross-chain compatibility
- Layer 2 scaling solutions

## 📞 Support

For blockchain-related issues:
1. Check the troubleshooting section
2. Review Django logs
3. Verify contract deployment
4. Test with local network first