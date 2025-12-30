#!/usr/bin/env python3
"""
Script to deploy smart contracts and update Django configuration
"""
import os
import sys
import json
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


def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None


def install_dependencies():
    """Install contract dependencies"""
    contracts_dir = project_root / 'contracts'
    
    print("Installing contract dependencies...")
    
    # Check if node_modules exists
    if not (contracts_dir / 'node_modules').exists():
        print("Installing npm packages...")
        result = run_command('npm install', cwd=contracts_dir)
        if result is None:
            print("Failed to install npm packages")
            return False
    
    return True


def compile_contracts():
    """Compile smart contracts"""
    contracts_dir = project_root / 'contracts'
    
    print("Compiling smart contracts...")
    result = run_command('npx hardhat compile', cwd=contracts_dir)
    
    if result is None:
        print("Failed to compile contracts")
        return False
    
    print("Contracts compiled successfully")
    return True


def deploy_contracts(network='localhost'):
    """Deploy contracts to specified network"""
    contracts_dir = project_root / 'contracts'
    
    print(f"Deploying contracts to {network}...")
    
    # Create deployments directory if it doesn't exist
    deployments_dir = contracts_dir / 'deployments'
    deployments_dir.mkdir(exist_ok=True)
    
    # Deploy contracts
    deploy_command = f'npx hardhat run scripts/deploy.js --network {network}'
    result = run_command(deploy_command, cwd=contracts_dir)
    
    if result is None:
        print("Failed to deploy contracts")
        return None
    
    # Read deployment info
    deployment_file = deployments_dir / f'{network}.json'
    if deployment_file.exists():
        with open(deployment_file, 'r') as f:
            deployment_info = json.load(f)
        return deployment_info
    else:
        print("Deployment file not found")
        return None


def update_django_config(deployment_info, network):
    """Update Django blockchain configuration with deployed contract addresses"""
    try:
        # Get or create blockchain config
        config, created = BlockchainConfig.objects.get_or_create(
            name=f'{network.title()} Network',
            defaults={
                'network_type': network,
                'rpc_url': 'http://127.0.0.1:8545' if network == 'localhost' else f'https://{network}.infura.io/v3/YOUR_PROJECT_ID',
                'chain_id': 1337 if network == 'localhost' else 11155111,  # Sepolia
                'is_active': True
            }
        )
        
        # Update contract addresses
        config.carbon_token_address = deployment_info['carbonToken']
        config.marketplace_address = deployment_info['marketplace']
        config.save()
        
        print(f"Django configuration updated:")
        print(f"  Carbon Token: {config.carbon_token_address}")
        print(f"  Marketplace: {config.marketplace_address}")
        
        return True
        
    except Exception as e:
        print(f"Failed to update Django configuration: {e}")
        return False


def main():
    """Main deployment function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy carbon credit smart contracts')
    parser.add_argument(
        '--network', 
        default='localhost', 
        choices=['localhost', 'sepolia', 'goerli', 'mainnet'],
        help='Network to deploy to'
    )
    parser.add_argument(
        '--skip-install', 
        action='store_true',
        help='Skip npm package installation'
    )
    parser.add_argument(
        '--skip-compile', 
        action='store_true',
        help='Skip contract compilation'
    )
    
    args = parser.parse_args()
    
    print("🚀 Carbon Credit Contract Deployment")
    print("=" * 40)
    
    # Install dependencies
    if not args.skip_install:
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            return 1
        print("✅ Dependencies installed")
    
    # Compile contracts
    if not args.skip_compile:
        if not compile_contracts():
            print("❌ Failed to compile contracts")
            return 1
        print("✅ Contracts compiled")
    
    # Deploy contracts
    deployment_info = deploy_contracts(args.network)
    if not deployment_info:
        print("❌ Failed to deploy contracts")
        return 1
    
    print("✅ Contracts deployed successfully")
    
    # Update Django configuration
    if update_django_config(deployment_info, args.network):
        print("✅ Django configuration updated")
    else:
        print("⚠️  Failed to update Django configuration")
    
    print("\n🎉 Deployment completed!")
    print("\nNext steps:")
    print("1. Run Django migrations: python manage.py migrate")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Start the Django server: python manage.py runserver")
    
    if args.network == 'localhost':
        print("\nFor local development:")
        print("- Make sure Hardhat node is running: npx hardhat node")
        print("- Import test accounts into MetaMask using the private keys from Hardhat")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())