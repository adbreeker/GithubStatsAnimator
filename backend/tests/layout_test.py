"""Quick layout test"""
import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join('..', '.env'))
sys.path.insert(0, '..')

from utils.account_general_generator import create_account_general_svg

async def test():
    username = os.getenv('GITHUB_USERNAME', 'adbreeker')
    svg = await create_account_general_svg(
        username=username,
        icon='github+streak',
        theme='dark'
    )
    
    # Ensure results directory exists (absolute path)
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    output_path = os.path.join(results_dir, 'improved_layout_test.svg')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    
    print('✅ Improved layout test generated')

asyncio.run(test())
