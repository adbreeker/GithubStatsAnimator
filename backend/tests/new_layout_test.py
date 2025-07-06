"""Test new card layout with different sizes"""
import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join('..', '.env'))
sys.path.insert(0, '..')

from utils.account_general_generator import create_account_general_svg

async def test_new_layout():
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    
    # Ensure results directory exists (absolute path)
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Test different sizes and configurations
    configs = [
        {
            'name': 'new_layout_default',
            'theme': 'dark',
            'width': 450,
            'height': 200,
            'icon': 'default'
        },
        {
            'name': 'new_layout_flip', 
            'theme': 'dark',
            'width': 450,
            'height': 200,
            'icon': 'default+github'
        },
        {
            'name': 'new_layout_large',
            'theme': 'dark',
            'width': 600,
            'height': 250,
            'icon': 'github+streak'
        },
        {
            'name': 'new_layout_compact',
            'theme': 'light',
            'width': 400,
            'height': 180,
            'icon': 'streak'
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
        
        output_path = os.path.join(results_dir, f"{config['name']}.svg")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        
        print(f"✅ {config['name']} generated ({config['width']}x{config['height']})")
    
    print("🎨 All new layout tests generated!")

asyncio.run(test_new_layout())
