#!/usr/bin/env python3
"""
Setup script for real blockchain integration
"""
import os
import sys
import subprocess
from pathlib import Path

# Add Django project to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from api.models import BlockchainConfig
from api.blockchain_service import BlockchainService


def run_command(command, cwd=None, check=True):
    """Run a shell command"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=check
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return None, e.stderr


def check_node_installed():
    """Check if Node.js is installed"""
    stdout, stderr = run_command('node --version', check=False)
    if stdout:
        print(f"✅ Node.js installed: {stdout}")
        return True
    else:
        print("❌ Node.js not found. Please install Node.js from https://nodejs.org/")
        return False


def setup_contracts():
    """Setup and install contract dependencies"""
    contracts_dir = project_root / 'contracts'
    
    print("\n📦 Setting up smart contracts...")
    
    # Check if contracts directory exists
    if not contracts_dir.exists():
        print("❌ Contracts directory not found")
        return False
    
    # Install npm dependencies
    print("Installing npm dependencies...")
    stdout, stderr = run_command('npm install', cwd=contracts_dir, check=False)
    
    if stderr and 'error' in stderr.lower():
        print(f"❌ npm install failed: {stderr}")
        return False
    
    print("✅ Contract dependencies installed")
    return True


def start_local_blockchain():
    """Start local Hardhat blockchain"""
    contracts_dir = project_root / 'contracts'
    
    print("\n🚀 Starting local blockchain...")
    print("Note: This will start Hardhat node in the background")
    
    # Start hardhat node in background
    try:
        process = subprocess.Popen(
            ['npx', 'hardhat', 'node'],
            cwd=contracts_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for it to start
        import time
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Local blockchain started successfully")
            print(f"   Process ID: {process.pid}")
            print("   Network: http://127.0.0.1:8545")
            print("   Chain ID: 1337")
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Failed to start blockchain: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting blockchain: {e}")
        return False


def deploy_contracts():
    """Deploy smart contracts to local network"""
    contracts_dir = project_root / 'contracts'
    
    print("\n📋 Deploying smart contracts...")
    
    stdout, stderr = run_command('npx hardhat run scripts/deploy.js --network localhost', cwd=contracts_dir, check=False)
    
    if stderr and 'error' in stderr.lower():
        print(f"❌ Contract deployment failed: {stderr}")
        return False
    
    if stdout:
        print("✅ Contracts deployed successfully")
        print(stdout)
        return True
    
    return False


def update_django_config():
    """Update Django blockchain configuration"""
    print("\n⚙️  Updating Django configuration...")
    
    try:
        # Check if configuration exists
        config = BlockchainConfig.get_active_config()
        
        if config:
            print(f"✅ Blockchain configuration found: {config.name}")
            print(f"   Network: {config.network_type}")
            print(f"   RPC URL: {config.rpc_url}")
            print(f"   Chain ID: {config.chain_id}")
            
            if config.carbon_token_address and config.marketplace_address:
                print("✅ Smart contracts configured")
                print(f"   Carbon Token: {config.carbon_token_address}")
                print(f"   Marketplace: {config.marketplace_address}")
            else:
                print("⚠️  Smart contract addresses not configured")
                print("   Please deploy contracts and update addresses in Django admin")
        else:
            print("⚠️  No blockchain configuration found")
            print("   Run: python manage.py setup_blockchain --network local --generate-key")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking Django config: {e}")
        return False


def test_blockchain_connection():
    """Test blockchain connection"""
    print("\n🔍 Testing blockchain connection...")
    
    try:
        status = BlockchainService.get_blockchain_status()
        
        if status.get('connected'):
            print("✅ Blockchain connection successful")
            print(f"   Network: {status.get('network')}")
            print(f"   Chain ID: {status.get('chain_id')}")
        else:
            print("❌ Blockchain connection failed")
            if 'error' in status:
                print(f"   Error: {status['error']}")
        
        return status.get('connected', False)
        
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Real Blockchain Setup for Carbon Credit Marketplace")
    print("=" * 60)
    
    # Check prerequisites
    if not check_node_installed():
        return 1
    
    # Setup contracts
    if not setup_contracts():
        return 1
    
    # Update Django config
    if not update_django_config():
        return 1
    
    # Test connection
    if not test_blockchain_connection():
        print("\n⚠️  Blockchain not connected. Starting local blockchain...")
        
        # Start local blockchain
        if not start_local_blockchain():
            return 1
        
        # Deploy contracts
        if not deploy_contracts():
            print("⚠️  Contract deployment failed, but blockchain is running")
            print("   You can deploy manually: cd contracts && npx hardhat run scripts/deploy.js --network localhost")
        
        # Test again
        if not test_blockchain_connection():
            print("❌ Still unable to connect to blockchain")
            return 1
    
    print("\n🎉 Real Blockchain Setup Complete!")
    print("\nNext steps:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Login as admin and approve a project to test credit minting")
    print("3. Check blockchain explorer: http://localhost:8000/blockchain/")
    print("4. All transactions will now be real blockchain transactions!")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())