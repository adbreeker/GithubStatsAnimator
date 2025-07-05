# GitHub Stats Animator Backend

A Flask-based REST API for generating animated GitHub contribution graphs.

## Project Structure

```
backend/
├── start.py                           # Main application entry point
├── api_registry.py                    # Central API route registration
├── requirements.txt                   # Python dependencies
├── .env                              # Environment variables (not in repo)
├── api_handlers/                     # API endpoint handlers
│   ├── __init__.py
│   └── contribution_graph_handler.py # Contribution graph API handler
└── utils/                           # Utility modules
    ├── __init__.py
    ├── chars_patterns.py            # Character patterns for text animation
    └── github_svg_generator.py      # SVG generation logic
```

## Quick Start

1. **Environment Setup**
   ```bash
   # Make sure your .env file contains:
   GITHUB_TOKEN=your_github_token_here
   GITHUB_USERNAME=your_github_username
   DEBUG=True
   PORT=5000
   HOST=0.0.0.0
   ```

2. **Start the Server**
   ```bash
   python start.py
   ```

3. **Test the API**
   ```bash
   # Health check
   GET http://localhost:5000/health
   
   # API info
   GET http://localhost:5000/api/info
   
   # Generate contribution graph
   GET http://localhost:5000/api/contribution-graph?username=octocat
   ```

## API Endpoints

### GET /health
Returns server health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "github-stats-animator"
}
```

### GET /api/info
Returns API information and available endpoints.

**Response:**
```json
{
  "service": "GitHub Stats Animator Backend",
  "version": "1.0.0",
  "endpoints": [...]
}
```

### GET /api/contribution-graph
Generates an animated GitHub contribution graph SVG.

**Parameters:**
- `theme` (optional): `light` or `dark` (default: `dark`)
- `text` (optional): Text to animate (default: `ADBREEKER`)
- `animation_time` (optional): Animation duration in seconds (default: `8.0`)
- `pause_time` (optional): Pause between cycles in seconds (default: `0.0`)
- `line_color` (optional): Color of eating lines in hex (default: `#ff8c00`)
- `line_alpha` (optional): Transparency of lines 0.0-1.0 (default: `0.7`)
- `square_size` (optional): Size of contribution squares in pixels (default: `11`)

**Note:** GitHub username is automatically read from the `GITHUB_USERNAME` environment variable.

**Example URLs:**
```
# Basic usage
GET /api/contribution-graph

# With custom text and theme
GET /api/contribution-graph?theme=light&text=HELLO

# Full customization
GET /api/contribution-graph?theme=dark&text=CODE&line_color=%23ff0000&line_alpha=0.9&square_size=12&animation_time=10.0&pause_time=2.0
```

### GET /api/top-languages
Generates a GitHub top languages SVG chart.

**Parameters:**
- `theme` (optional): `light` or `dark` (default: `dark`)
- `limit` (optional): Number of languages to show (default: `5`, max: `20`)
- `width` (optional): SVG width in pixels (default: `400`, range: `200-1000`)
- `height` (optional): SVG height in pixels (default: `300`, range: `150-800`)
- `show_percentages` (optional): Show percentage labels (default: `true`)
- `title` (optional): Custom title (default: `Most Used Languages`)

**Note:** GitHub username is automatically read from the `GITHUB_USERNAME` environment variable.

**Example URLs:**
```
# Basic usage
GET /api/top-languages

# Custom size and theme
GET /api/top-languages?theme=light&width=500&height=400

# Show more languages with custom title
GET /api/top-languages?limit=8&title=My%20Programming%20Languages

# Full customization
GET /api/top-languages?theme=dark&limit=10&width=600&height=500&show_percentages=false&title=Code%20Distribution
```

**Response:**
- Content-Type: `image/svg+xml`
- Returns SVG chart showing top programming languages with percentages

## Architecture

### Modular Design
- **start.py**: Application entry point with configuration
- **api_registry.py**: Central route registration for easy expansion
- **api_handlers/**: Individual handler modules for each API endpoint
- **utils/**: Reusable utility modules

### Easy Expansion
To add a new API endpoint:

1. Create a new handler in `api_handlers/`:
   ```python
   # api_handlers/new_feature_handler.py
   def register_new_feature_routes(app):
       @app.route('/api/new-feature', methods=['GET'])
       def get_new_feature():
           return {"message": "New feature"}, 200
   ```

2. Register it in `api_registry.py`:
   ```python
   from api_handlers.new_feature_handler import register_new_feature_routes
   
   def register_all_routes(app):
       register_contribution_graph_routes(app)
       register_new_feature_routes(app)  # Add this line
   ```

### Error Handling
The API includes comprehensive error handling:
- Parameter validation with detailed error messages
- GitHub API error handling
- Environment variable validation
- SVG generation error handling

## Development

### Testing
Run the setup test:
```bash
python test_setup.py
```

### Adding Features
1. Create new handlers in `api_handlers/`
2. Add utilities to `utils/` if needed
3. Register routes in `api_registry.py`
4. Update this README

### Environment Variables
- `GITHUB_TOKEN`: GitHub personal access token
- `GITHUB_USERNAME`: Default GitHub username
- `DEBUG`: Enable debug mode (True/False)
- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: 0.0.0.0)

## Features

- ✅ Clean, modular architecture
- ✅ Easy to extend with new APIs
- ✅ Comprehensive error handling
- ✅ CORS enabled for frontend integration
- ✅ Environment-based configuration
- ✅ SVG response with proper content types
- ✅ Parameter validation
- ✅ Health check endpoints
- ✅ API documentation endpoint
