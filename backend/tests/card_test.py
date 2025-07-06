"""Test new card design with different themes and sizes"""
import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join('..', '.env'))
sys.path.insert(0, '..')

from utils.account_general_generator import create_account_general_svg

async def test_card_designs():
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    
    # Ensure results directory exists (absolute path)
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Test different configurations
    configs = [
        {
            'name': 'dark_card',
            'theme': 'dark',
            'width': 500,
            'height': 200,
            'icon': 'default'
        },
        {
            'name': 'light_card', 
            'theme': 'light',
            'width': 500,
            'height': 200,
            'icon': 'github'
        },
        {
            'name': 'streak_card',
            'theme': 'dark',
            'width': 500,
            'height': 200,
            'icon': 'streak'
        },
        {
            'name': 'large_card',
            'theme': 'dark',
            'width': 600,
            'height': 250,
            'icon': 'default+github'
        }
    ]
    
    for config in configs:
        print(f"Generating {config['name']}...")
        svg = await create_account_general_svg(
            username=username,
            theme=config['theme'],
            width=config['width'],
            height=config['height'],
            icon=config['icon']
        )
        
        output_path = os.path.join(results_dir, f"card_{config['name']}.svg")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        
        print(f"✅ {config['name']} generated")
    
    print("🎉 All card designs generated!")

asyncio.run(test_card_designs())
