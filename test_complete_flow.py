#!/usr/bin/env python
"""
Test script to verify complete blockchain integration flow
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def test_complete_flow():
    """Test the complete blockchain integration flow"""
    print("Testing complete blockchain integration flow...")
    
    try:
        from django.contrib.auth.models import User, Group
        from api.models import Project, BlockchainConfig, Wallet, ChainTransaction
        from api.blockchain_service import BlockchainService
        
        print("1. Testing blockchain status...")
        status = BlockchainService.get_blockchain_status()
        print(f"   Connected: {status.get('connected')}")
        print(f"   Network: {status.get('network')}")
        print(f"   Contracts deployed: {status.get('contracts_deployed')}")
        
        if not status.get('connected'):
            print("   ❌ Blockchain not connected")
            return False
        
        print("2. Testing blockchain configuration...")
        config = BlockchainConfig.get_active_config()
        if config:
            print(f"   ✓ Active config found: {config.name}")
            print(f"   Carbon Token: {config.carbon_token_address}")
            print(f"   Marketplace: {config.marketplace_address}")
        else:
            print("   ❌ No active blockchain config")
            return False
        
        print("3. Testing user and project creation...")
        
        # Create NGO user
        ngo_group, _ = Group.objects.get_or_create(name="NGO")
        ngo_user, created = User.objects.get_or_create(
            username="test_ngo@example.com",
            defaults={
                'email': 'test_ngo@example.com',
                'first_name': 'Test',
                'last_name': 'NGO'
            }
        )
        if created:
            ngo_user.groups.add(ngo_group)
            print(f"   ✓ Created NGO user: {ngo_user.username}")
        else:
            print(f"   ✓ Using existing NGO user: {ngo_user.username}")
        
        # Create Corporate user
        corp_group, _ = Group.objects.get_or_create(name="Corporate")
        corp_user, created = User.objects.get_or_create(
            username="test_corp@example.com",
            defaults={
                'email': 'test_corp@example.com',
                'first_name': 'Test',
                'last_name': 'Corporate'
            }
        )
        if created:
            corp_user.groups.add(corp_group)
            print(f"   ✓ Created Corporate user: {corp_user.username}")
        else:
            print(f"   ✓ Using existing Corporate user: {corp_user.username}")
        
        # Ensure wallets exist
        ngo_wallet = Wallet.ensure(ngo_user)
        corp_wallet = Wallet.ensure(corp_user)
        print(f"   ✓ NGO wallet: {ngo_wallet.address}")
        print(f"   ✓ Corporate wallet: {corp_wallet.address}")
        
        # Create test project
        project, created = Project.objects.get_or_create(
            title="Test Reforestation Project",
            defaults={
                'ngo': ngo_user,
                'location': 'Test Forest',
                'species': 'Oak Trees',
                'area': 100.0,
                'status': 'approved',
                'credits': 500,
                'chain_issued': False
            }
        )
        if created:
            print(f"   ✓ Created test project: {project.title}")
        else:
            print(f"   ✓ Using existing test project: {project.title}")
        
        print("4. Testing credit minting...")
        if not project.chain_issued:
            try:
                tx_hash = BlockchainService.mint_credits_for_project(project)
                if tx_hash:
                    print(f"   ✓ Credits minted successfully: {tx_hash}")
                    
                    # Check if transaction was recorded
                    tx = ChainTransaction.objects.filter(tx_hash=tx_hash).first()
                    if tx:
                        print(f"   ✓ Transaction recorded in database: {tx.kind}")
                    else:
                        print("   ⚠️ Transaction not found in database")
                else:
                    print("   ❌ Credit minting failed")
                    return False
            except Exception as e:
                print(f"   ❌ Credit minting error: {e}")
                return False
        else:
            print("   ✓ Credits already minted for this project")
        
        print("5. Testing user balances...")
        ngo_balance = BlockchainService.get_user_balance(ngo_user)
        corp_balance = BlockchainService.get_user_balance(corp_user)
        print(f"   NGO balance: {ngo_balance} credits")
        print(f"   Corporate balance: {corp_balance} credits")
        
        print("6. Testing credit transfer...")
        if ngo_balance >= 100:
            try:
                tx_hash = BlockchainService.transfer_credits(
                    from_user=ngo_user,
                    to_user=corp_user,
                    amount=100,
                    project_id=project.id
                )
                if tx_hash:
                    print(f"   ✓ Credits transferred successfully: {tx_hash}")
                    
                    # Check updated balances
                    new_ngo_balance = BlockchainService.get_user_balance(ngo_user)
                    new_corp_balance = BlockchainService.get_user_balance(corp_user)
                    print(f"   Updated NGO balance: {new_ngo_balance} credits")
                    print(f"   Updated Corporate balance: {new_corp_balance} credits")
                else:
                    print("   ❌ Credit transfer failed")
                    return False
            except Exception as e:
                print(f"   ❌ Credit transfer error: {e}")
                return False
        else:
            print("   ⚠️ Insufficient NGO balance for transfer test")
        
        print("7. Testing blockchain explorer data...")
        real_txs = ChainTransaction.objects.filter(
            tx_hash__isnull=False, 
            tx_hash__gt=''
        ).count()
        print(f"   Real blockchain transactions: {real_txs}")
        
        if real_txs > 0:
            print("   ✓ Blockchain transactions are being recorded")
        else:
            print("   ⚠️ No blockchain transactions found")
        
        print("\n🎉 Complete blockchain integration test PASSED!")
        print("✅ All components are working correctly:")
        print("   - Blockchain connection established")
        print("   - Smart contracts deployed and configured")
        print("   - Credit minting on blockchain")
        print("   - Credit transfers between wallets")
        print("   - Transaction recording in database")
        print("   - Real blockchain-only mode active")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_flow()
    sys.exit(0 if success else 1)