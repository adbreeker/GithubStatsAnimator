# GitHub Stats Animator - Vercel Deployment

This project is configured for deployment on Vercel with a React frontend and Python serverless backend.

## Project Structure

```
├── api/                    # Vercel Serverless Functions (Python)
│   ├── account-general.py  # Account stats API
│   ├── contributions-graph.py # Contributions graph API  
│   ├── top-languages.py    # Top languages API
│   └── utils/              # Shared utilities
├── frontend/               # React frontend
│   ├── src/
│   ├── dist/              # Build output
│   └── package.json
├── backend/               # Original Flask backend (for local dev)
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies for API
└── package.json         # Root package.json for build
```

## Local Development

### Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python start.py
```

### Frontend (React)  
```bash
cd frontend
npm install
npm run dev
```

### Full Stack Development
```bash
npm install # Install concurrently
npm run dev # Runs both frontend and backend
```

## Vercel Deployment

### 1. Environment Variables

Set these in your Vercel dashboard:

- `GITHUB_USERNAME` - Your GitHub username (required)
- `GITHUB_TOKEN` - GitHub Personal Access Token (optional, for higher rate limits)

### 2. Deploy to Vercel

#### Option A: Vercel CLI
```bash
npm install -g vercel
vercel --prod
```

#### Option B: Git Integration
1. Connect your GitHub repository to Vercel
2. Vercel will automatically deploy on push to main branch

### 3. API Endpoints

Once deployed, your API will be available at:

- `https://your-app.vercel.app/api/account-general`
- `https://your-app.vercel.app/api/top-languages`  
- `https://your-app.vercel.app/api/contributions-graph`

## API Usage

### Account General Stats
```
GET /api/account-general?theme=dark&icon=default&slot1=stars&slot2=commits_total
```

### Top Languages
```
GET /api/top-languages?theme=dark&languages_count=5&width=400&height=300
```

### Contributions Graph
```
GET /api/contributions-graph?theme=dark&text=HELLO&animation_time=8.0
```

## Frontend Features

- Real-time preview of GitHub stats
- Live connection to backend API
- Configuration interface for all parameters
- Responsive design
- Error handling and loading states

## Architecture Benefits

### Serverless Functions vs Traditional Backend

✅ **Pros:**
- **No API rate limits** - Each function call runs independently
- **Cost effective** - Pay per request, not for idle server time
- **Auto-scaling** - Handles traffic spikes automatically
- **Zero maintenance** - No server management required
- **Fast cold starts** - Python functions start quickly
- **Global edge deployment** - Low latency worldwide

❌ **Cons:**
- 10-second execution timeout per function
- Memory limits (1GB max)
- Cold start delays (minimal with Python)

### Performance Optimization

The current setup is optimized for Vercel's serverless environment:

1. **Shared utilities** - Copied to `/api/utils` to avoid import issues
2. **Minimal dependencies** - Only essential packages in requirements.txt
3. **Direct SVG response** - No JSON wrapper for better performance
4. **Frontend caching** - Vite optimizations for static assets
5. **CORS handling** - Proper headers for cross-origin requests

## Troubleshooting

### Common Issues

1. **Import errors in API functions**
   - Ensure `utils/` directory is copied to `/api/utils/`
   - Check Python path configurations

2. **Environment variables not found**
   - Set `GITHUB_USERNAME` in Vercel dashboard
   - Add `GITHUB_TOKEN` for higher rate limits

3. **CORS errors**
   - API functions include proper CORS headers
   - Check browser developer tools for specific errors

4. **Function timeouts**
   - GitHub API calls should complete within 10 seconds
   - Consider caching for heavy operations

### Local Testing

Test API functions locally:
```bash
cd api
python -c "from contributions_graph import handler; print('Import successful')"
```

## Production Considerations

1. **Rate Limiting** - Add GitHub token for higher API limits
2. **Caching** - Consider adding Redis for frequently requested stats  
3. **Monitoring** - Use Vercel Analytics for performance tracking
4. **Error Logging** - Add proper error logging and alerting
5. **Security** - Validate all input parameters thoroughly

## Migration from Flask

The original Flask backend (`/backend`) is preserved for local development. Key changes for Vercel:

1. Flask routes → Serverless functions
2. Single app.py → Multiple endpoint files
3. Shared imports → Copied utilities
4. Environment config → Vercel environment variables

This architecture provides the best of both worlds: easy local development with Flask and production-ready serverless deployment on Vercel.
