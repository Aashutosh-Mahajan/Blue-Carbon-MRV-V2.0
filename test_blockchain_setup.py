#!/usr/bin/env python
"""
Test script to verify blockchain auto-setup functionality
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

def test_blockchain_auto_setup():
    """Test the blockchain auto-setup functionality"""
    print("Testing blockchain auto-setup...")
    
    try:
        from api.blockchain_auto_setup import BlockchainAutoSetup
        
        # Create auto-setup instance
        setup = BlockchainAutoSetup()
        
        # Test blockchain connection check
        print("1. Testing blockchain connection check...")
        is_running = setup._check_blockchain_running()
        print(f"   Blockchain running: {is_running}")
        
        if not is_running:
            print("2. Testing blockchain startup...")
            success = setup._start_local_blockchain()
            print(f"   Blockchain started: {success}")
            
            if success:
                print("3. Testing contract deployment...")
                deployed = setup._deploy_contracts()
                print(f"   Contracts deployed: {deployed}")
                
                if deployed:
                    print("4. Testing Django config update...")
                    setup._update_django_config()
                    print("   Django config updated")
                    
                    # Check if config was created
                    from api.models import BlockchainConfig
                    config = BlockchainConfig.get_active_config()
                    if config:
                        print(f"   Carbon Token: {config.carbon_token_address}")
                        print(f"   Marketplace: {config.marketplace_address}")
                    else:
                        print("   No active blockchain config found")
        
        print("\nTest completed!")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        try:
            if hasattr(setup, 'blockchain_process') and setup.blockchain_process:
                setup.stop_blockchain()
        except:
            pass

if __name__ == "__main__":
    test_blockchain_auto_setup()