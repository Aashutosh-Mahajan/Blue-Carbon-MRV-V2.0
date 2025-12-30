#!/usr/bin/env python3
"""
Demo script to showcase blockchain functionality
"""
import os
import sys
from pathlib import Path

# Add Django project to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from api.blockchain_service import BlockchainService
from api.models import BlockchainConfig, Wallet
from django.contrib.auth.models import User


def main():
    print("🚀 Carbon Credit Blockchain Demo")
    print("=" * 50)
    
    # Check blockchain status
    print("\n1. Checking Blockchain Status...")
    status = BlockchainService.get_blockchain_status()
    print(f"   Connected: {status.get('connected', False)}")
    print(f"   Network: {status.get('network', 'unknown')}")
    if 'error' in status:
        print(f"   Note: {status['error']}")
    
    # Show blockchain configuration
    print("\n2. Blockchain Configuration...")
    config = BlockchainConfig.get_active_config()
    if config:
        print(f"   Name: {config.name}")
        print(f"   Network: {config.network_type}")
        print(f"   RPC URL: {config.rpc_url}")
        print(f"   Chain ID: {config.chain_id}")
        print(f"   Contracts Deployed: {bool(config.carbon_token_address and config.marketplace_address)}")
        if config.carbon_token_address:
            print(f"   Carbon Token: {config.carbon_token_address}")
        if config.marketplace_address:
            print(f"   Marketplace: {config.marketplace_address}")
    else:
        print("   No blockchain configuration found")
    
    # Test wallet creation
    print("\n3. Testing Wallet Creation...")
    try:
        # Create a test user if it doesn't exist
        test_user, created = User.objects.get_or_create(
            username='blockchain_test_user',
            defaults={
                'email': 'test@blockchain.com',
                'first_name': 'Blockchain',
                'last_name': 'Tester'
            }
        )
        
        # Ensure wallet exists
        wallet = Wallet.ensure(test_user)
        print(f"   Test User: {test_user.username}")
        print(f"   Wallet Address: {wallet.address}")
        print(f"   Is External: {wallet.is_external}")
        
        # Get balance
        balance = BlockchainService.get_user_balance(test_user)
        print(f"   Token Balance: {balance} CCT")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Show available features
    print("\n4. Available Blockchain Features...")
    features = [
        "✅ ERC20 Carbon Credit Token (CCT)",
        "✅ Project registration on blockchain",
        "✅ Automated credit minting for approved projects",
        "✅ Credit transfers between users",
        "✅ Marketplace for credit trading",
        "✅ Tender system with smart contracts",
        "✅ Real-time balance tracking",
        "✅ Transaction history and verification",
        "✅ Multi-network support (Local, Sepolia, Mainnet)",
        "✅ Fallback to simple blockchain for development"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print("\n5. Next Steps...")
    steps = [
        "1. Start local blockchain: cd contracts && npx hardhat node",
        "2. Deploy contracts: python scripts/deploy_contracts.py --network localhost",
        "3. Update contract addresses in Django admin",
        "4. Create projects and test credit minting",
        "5. Test credit transfers and marketplace"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🎉 Blockchain integration is ready!")
    print("   Check the admin panel for blockchain management")
    print("   Visit /api/blockchain/status/ for real-time status")


if __name__ == '__main__':
    main()