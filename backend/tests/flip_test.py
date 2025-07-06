"""Test coin flip animations specifically"""
import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join('..', '.env'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.account_general_generator import create_account_general_svg

async def test_coin_flips():
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    
    # Ensure results directory exists (absolute path)
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Test different coin flip combinations
    flip_configs = [
        {
            'name': 'default_github_flip',
            'icon': 'default+github'
        },
        {
            'name': 'github_streak_flip', 
            'icon': 'github+streak'
        },
        {
            'name': 'default_streak_flip',
            'icon': 'default+streak'
        }
    ]
    
    for config in flip_configs:
        print(f"Generating {config['name']}...")
        svg = await create_account_general_svg(
            username=username,
            icon=config['icon'],
            theme='dark'
        )
        
        output_path = os.path.join(results_dir, f"flip_{config['name']}.svg")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        
        print(f"✅ {config['name']} generated")
    
    print("🪙 All coin flip tests generated!")

asyncio.run(test_coin_flips())
