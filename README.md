# 🎬 GitHub Stats Animator

[![GitHub license](https://img.shields.io/github/license/adbreeker/GithubStatsAnimator)](https://github.com/adbreeker/GithubStatsAnimator/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/adbreeker/GithubStatsAnimator)](https://github.com/adbreeker/GithubStatsAnimator/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/adbreeker/GithubStatsAnimator)](https://github.com/adbreeker/GithubStatsAnimator/network)

Dynamically updated animated GitHub stats generator with customizable SVG outputs. Features a React frontend for configuration and Python backend APIs for generating animated contribution graphs, language stats, and profile cards with beautiful smooth animations.

> **⚠️ Important Note for Users:** 
> This public deployment is configured for a specific user due to Vercel's limited API calls. **For generating stats for your own GitHub profile, it's highly recommended to deploy your own instance by following the [Personal Deployment Tutorial](#-personal-deployment-on-vercel)** below.

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Live Demo](#-live-demo)
- [🖼️ Examples](#️-examples)
- [📚 API Endpoints](#-api-endpoints)
- [🔧 Personal Deployment on Vercel](#-personal-deployment-on-vercel)
- [🏠 Local Development](#-local-development)
- [⚙️ Configuration](#️-configuration)
- [🎨 Customization](#-customization)
- [🌟 Inspiration](#-inspiration)
- [📄 License](#-license)

## ✨ Features

- **🎬 Animated SVG Generation**: Smooth animations for contribution graphs with customizable text overlays
- **📊 Multiple Stats Types**: 
  - Account general stats (stars, commits, PRs, issues, etc.)
  - Top programming languages with percentages
  - Animated contributions graph with custom text
- **🎨 Theme Support**: Light and dark themes with customizable colors
- **⚡ Live Preview**: Real-time configuration with instant preview in React frontend
- **🔄 Dynamic Updates**: Real-time data fetching from GitHub GraphQL API
- **🎯 Customizable Elements**:
  - Animation timing and colors
  - Text overlays on contribution graphs
  - Icon types (user avatar, GitHub logo, streak counter)
  - Color schemes and transparency
- **📱 Responsive Design**: Modern React frontend with CSS modules
- **🚀 Easy Deployment**: Pre-configured for Vercel with environment variables
- **🔗 Direct API Access**: RESTful endpoints for direct SVG generation

## 🚀 Live Demo

Visit the live demo: [GitHub Stats Animator](https://your-vercel-deployment.vercel.app)

## 🖼️ Examples

### Account General Stats
```html
<img src="https://your-deployment.vercel.app/api/account-general?theme=dark&icon=default+github" alt="GitHub Stats" />
```

### Top Languages
```html
<img src="https://your-deployment.vercel.app/api/top-languages?theme=dark&languages_count=8" alt="Top Languages" />
```

### Animated Contributions Graph
```html
<img src="https://your-deployment.vercel.app/api/contributions-graph?theme=dark&text=CODING&animation_time=10" alt="Contributions Graph" />
```

## 📚 API Endpoints

All API endpoints return SVG content that can be directly embedded in HTML or Markdown.

### `/api/account-general`
Generate general account statistics card.

**Parameters:**
- `theme` - `light` | `dark` (default: `dark`)
- `icon` - `default` | `user` | `github` | `streak` | combinations with `+` (default: `default`)
- `slot1-5` - Statistics to display: `stars`, `commits_total`, `commits_year`, `pull_requests`, `code_reviews`, `issues`, `external_contributions`

### `/api/top-languages`
Generate top programming languages chart.

**Parameters:**
- `theme` - `light` | `dark` (default: `dark`)
- `languages_count` - Number of languages to show (default: `5`)
- `decimal_places` - Decimal places for percentages (default: `1`)
- `count_other_languages` - Include "Other" category (default: `false`)
- `exclude_languages` - Comma-separated list of languages to exclude

### `/api/contributions-graph`
Generate animated contributions graph.

**Parameters:**
- `theme` - `light` | `dark` (default: `dark`)
- `text` - Text to animate over the graph (default: `ADBREEKER`)
- `line_color` - Animation line color (default: `#ff8c00`)
- `line_alpha` - Line transparency 0-1 (default: `0.7`)
- `square_size` - Size of contribution squares (default: `11`)
- `animation_time` - Animation duration in seconds (default: `8.0`)
- `pause_time` - Pause between animations in seconds (default: `0.0`)

## 🔧 Personal Deployment on Vercel

To deploy your own instance and generate stats for your GitHub profile:

### Step 1: Fork the Repository
1. Visit this repository on GitHub
2. Click the **"Fork"** button in the top right corner
3. Select your GitHub account as the destination

### Step 2: Create GitHub Token
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Give it a descriptive name like "GitHub Stats Animator"
4. Select the following scopes:
   - `read:user` - Access to profile information
   - `repo:status` - Access to repository commit status
5. Click **"Generate token"** and copy the token (save it securely!)

### Step 3: Deploy on Vercel
1. Visit [Vercel](https://vercel.com) and sign in with your GitHub account
2. Click **"New Project"**
3. Import your forked repository
4. In the **"Configure Project"** section, add these Environment Variables:
   ```
   GITHUB_USERNAME=your-github-username
   GITHUB_TOKEN=your-generated-token
   ```
5. Click **"Deploy"**

### Step 4: Use Your Deployment
Once deployed, you can generate SVG links for your GitHub stats! Visit your deployment's main page to access the interactive editor where you can:

- **Configure your stats** with real-time preview
- **Customize themes, colors, and animations**
- **Copy ready-to-use SVG URLs** for your README

Or use the API endpoints directly:
```html
<img src="https://your-project-name.vercel.app/api/account-general" alt="My GitHub Stats" />
```

That's it! 🎉 Your personal GitHub Stats Animator is now live and ready to use.

## 🏠 Local Development

### Prerequisites
- Python 3.7+
- Node.js 16+
- GitHub Personal Access Token

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/adbreeker/GithubStatsAnimator.git
   cd GithubStatsAnimator
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```
   
3. **Configure environment variables:**
   ```env
   GITHUB_USERNAME=your-github-username
   GITHUB_TOKEN=your-github-token
   DEV_PORT=8000
   DEV_HOST=localhost
   ```

4. **Install dependencies:**
   ```bash
   # Backend dependencies
   pip install -r requirements.txt
   
   # Frontend dependencies
   cd frontend
   npm install
   cd ..
   ```

5. **Run development server:**
   ```bash
   npm run dev
   ```
   
   This starts both the Python backend and React frontend concurrently.

6. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend APIs: http://localhost:8000/api/*

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `GITHUB_USERNAME` | Your GitHub username | ✅ | `octocat` |
| `GITHUB_TOKEN` | GitHub Personal Access Token | ✅ | `ghp_xxxxxxxxxxxx` |
| `DEV_PORT` | Local development port | ❌ | `8000` |
| `DEV_HOST` | Local development host | ❌ | `localhost` |

### GitHub Token Permissions
Your GitHub token needs the following permissions:
- **read:user** - Access to profile information
- **repo:status** - Access to repository commit status
- **repo** - Access to private repositories (if you want to include stats from private repos)
- **read:org** (optional) - If you want to include organization data

> **⚠️ Security Warning about Private Repositories:** 
> 
> If you want your GitHub stats to include contributions from private repositories, you need to grant the **`repo`** scope instead of just `repo:status`. However, **using the `repo` scope is discouraged** as it gives full access to all your repositories (both public and private), including the ability to read, write, and delete repository content.
> 
> **If this token is ever leaked or compromised, it could cause significant harm to your private repositories.** For security reasons, it's recommended to:
> - Use only `repo:status` scope when possible
> - If you must use `repo` scope, ensure your deployment environment is secure
> - Regularly rotate your tokens
> - Consider the trade-off between comprehensive stats and security
> 
> The stats will still be aggregated and won't expose specific private repository details, but the token itself has broader permissions.

## 🎨 Customization

### Frontend Customization
The React frontend is built with:
- **Vite** for fast development and building
- **CSS Modules** for scoped styling
- **Modern React 19** with hooks

Key files for customization:
- `frontend/src/components/` - React components
- `frontend/src/styles/` - CSS module stylesheets
- `frontend/src/pages/MainPage.jsx` - Main application page

### Backend Customization
The Python backend provides:
- **GraphQL integration** with GitHub API
- **SVG generation** with custom animations
- **Modular utilities** for easy extension

Key files for customization:
- `api/utils/` - Core generation logic
- `api/*.py` - API endpoint handlers
- `api/utils/chars_patterns.py` - Character patterns for animations

### Adding New Stats Types
1. Add stat configuration in `api/utils/account_general_generator.py`
2. Implement fetching logic in the `GitHubAccountStatsAPI` class
3. Update frontend options in `frontend/src/components/StatsAttributes.jsx`

## 🌟 Inspiration

This project was initially inspired by [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats), which I used for several years before deciding to create my own version. While maintaining some similarities to the original concept, this project introduces tons of new features including:

- **Animated contributions graphs** with custom text overlays
- **Interactive React frontend** for real-time configuration
- **Modern technology stack** with React + Python backend
- **Enhanced performance** with optimized GraphQL queries
- **Expanded statistics** and visualization options

The goal was to create a more customizable, feature-rich, and modern alternative with nicely animated visuals using technologies closer to my heart while building upon the excellent foundation established by the original project.

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

The MIT License is a permissive license that allows you to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software with minimal restrictions.

---

<p align="center">
  Made with ❤️ and lots of ☕
</p>

<p align="center">
  <sub>Built with React, Python, and GitHub GraphQL API</sub>
</p>
