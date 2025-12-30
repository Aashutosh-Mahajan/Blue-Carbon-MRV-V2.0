#!/usr/bin/env python3
"""
Test script for blockchain explorer functionality
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
from api.models import ChainTransaction, Wallet, Project, BlockchainConfig
from django.contrib.auth.models import User


def create_test_data():
    """Create some test blockchain transactions"""
    print("Creating test blockchain data...")
    
    # Create test users
    ngo_user, _ = User.objects.get_or_create(
        username='test_ngo',
        defaults={'email': 'ngo@test.com', 'first_name': 'Test', 'last_name': 'NGO'}
    )
    
    corp_user, _ = User.objects.get_or_create(
        username='test_corp',
        defaults={'email': 'corp@test.com', 'first_name': 'Test', 'last_name': 'Corp'}
    )
    
    # Ensure wallets exist
    ngo_wallet = Wallet.ensure(ngo_user)
    corp_wallet = Wallet.ensure(corp_user)
    
    # Create test project
    project, _ = Project.objects.get_or_create(
        title='Test Mangrove Project',
        defaults={
            'ngo': ngo_user,
            'location': 'Test Location',
            'species': 'Mangrove',
            'area': 100.0,
            'credits': 500,
            'status': 'approved'
        }
    )
    
    # Create test transactions
    transactions = [
        {
            'sender': 'SYSTEM',
            'recipient': ngo_wallet.address,
            'amount': 500,
            'project_id': project.id,
            'kind': 'MINT',
            'meta': {
                'project_title': project.title,
                'ngo_username': ngo_user.username,
                'blockchain_type': 'real'
            },
            'tx_hash': '0x1234567890abcdef1234567890abcdef12345678'
        },
        {
            'sender': ngo_wallet.address,
            'recipient': corp_wallet.address,
            'amount': 100,
            'project_id': project.id,
            'kind': 'TRANSFER',
            'meta': {
                'from_username': ngo_user.username,
                'to_username': corp_user.username,
                'blockchain_type': 'real'
            },
            'tx_hash': '0xabcdef1234567890abcdef1234567890abcdef12'
        },
        {
            'sender': ngo_wallet.address,
            'recipient': corp_wallet.address,
            'amount': 50,
            'project_id': project.id,
            'kind': 'TRANSFER',
            'meta': {
                'from_username': ngo_user.username,
                'to_username': corp_user.username,
                'blockchain_type': 'simple'
            }
        }
    ]
    
    for tx_data in transactions:
        ChainTransaction.objects.get_or_create(
            tx_hash=tx_data.get('tx_hash', ''),
            sender=tx_data['sender'],
            recipient=tx_data['recipient'],
            defaults=tx_data
        )
    
    print(f"Created {len(transactions)} test transactions")
    return len(transactions)


def test_blockchain_explorer():
    """Test the blockchain explorer functionality"""
    print("\n🔍 Testing Blockchain Explorer Functionality")
    print("=" * 50)
    
    # Create test data
    tx_count = create_test_data()
    
    # Test blockchain status
    print("\n1. Testing Blockchain Status...")
    status = BlockchainService.get_blockchain_status()
    print(f"   Connected: {status.get('connected', False)}")
    print(f"   Network: {status.get('network', 'unknown')}")
    
    # Test transaction retrieval
    print("\n2. Testing Transaction Retrieval...")
    all_transactions = ChainTransaction.objects.all()
    real_blockchain_txs = all_transactions.filter(tx_hash__isnull=False, tx_hash__gt='')
    simple_blockchain_txs = all_transactions.filter(tx_hash__isnull=True) | all_transactions.filter(tx_hash='')
    
    print(f"   Total Transactions: {all_transactions.count()}")
    print(f"   Real Blockchain Transactions: {real_blockchain_txs.count()}")
    print(f"   Simple Blockchain Transactions: {simple_blockchain_txs.count()}")
    
    # Test transaction enrichment
    print("\n3. Testing Transaction Enrichment...")
    for tx in all_transactions[:3]:  # Test first 3 transactions
        print(f"   Transaction {tx.id}:")
        print(f"     Kind: {tx.kind}")
        print(f"     Amount: {tx.amount}")
        print(f"     Sender: {tx.sender[:20]}...")
        print(f"     Recipient: {tx.recipient[:20]}...")
        print(f"     TX Hash: {tx.tx_hash or 'N/A'}")
        print(f"     Project ID: {tx.project_id}")
        
        # Test wallet resolution
        try:
            sender_wallet = Wallet.objects.filter(address=tx.sender).first()
            recipient_wallet = Wallet.objects.filter(address=tx.recipient).first()
            print(f"     Sender User: {sender_wallet.user.username if sender_wallet else 'N/A'}")
            print(f"     Recipient User: {recipient_wallet.user.username if recipient_wallet else 'N/A'}")
        except Exception as e:
            print(f"     Wallet Resolution Error: {e}")
        print()
    
    # Test statistics calculation
    print("4. Testing Statistics Calculation...")
    total_credits_issued = sum(tx.amount for tx in all_transactions.filter(kind__in=['ISSUE', 'MINT']))
    total_credits_transferred = sum(tx.amount for tx in all_transactions.filter(kind='TRANSFER'))
    unique_wallets = Wallet.objects.count()
    total_projects = Project.objects.count()
    
    print(f"   Total Credits Issued: {total_credits_issued}")
    print(f"   Total Credits Transferred: {total_credits_transferred}")
    print(f"   Unique Wallets: {unique_wallets}")
    print(f"   Total Projects: {total_projects}")
    
    print("\n✅ Blockchain Explorer Test Complete!")
    print("\nTo view the explorer:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Login as admin")
    print("3. Visit: http://localhost:8000/blockchain/")


if __name__ == '__main__':
    test_blockchain_explorer()