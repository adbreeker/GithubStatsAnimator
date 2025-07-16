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

- **🎬 Animated SVG Generation**: Smooth, multi-phase animations for contribution graphs, stat cards, and counters, with customizable text overlays and pixel font effects.
- **📊 Multiple Stats Types**:
  - **Account General Card**: Stars, commits (total, year, 6 months), PRs, code reviews, issues, external contributions, and animated streak. Choose from 6 stat slots and 6 icon types (user, GitHub, streak, or any rotating combo).
  - **Top Languages Chart**: Fully animated, responsive SVG bar chart with emoji for top language, custom width/height, decimal places, "Other" category, and language exclusion.
  - **Animated Contributions Graph**: Custom text overlays using pixel font, multi-phase "eating line" animation, color/alpha/square size controls, and robust error handling.
  - **Views Counter**: Animated slot-machine SVG counter for profile views, with persistent counting (Postgres/Neon DB support, fallback to "a crapload" if no DB).
- **🎨 Theme Support**: Light and dark themes with customizable colors for all SVGs.
- **⚡ Live Preview**: Real-time configuration and instant SVG preview in the React frontend.
- **🔄 Dynamic Updates**: Real-time data fetching from GitHub GraphQL API for all stats.
- **🎯 Customizable Elements**:
  - Animation timing, icon rotation, and color/alpha controls
  - Text overlays and pixel font for contributions graph
  - Stat slot selection, icon types, and layout
  - Bar chart width/height, decimal places, and language exclusion
- **🔢 Views Counter**: Animated slot-machine style, persistent (Postgres/Neon DB) or fallback, with dark/light themes and accessibility.
- **🧪 Robust Testing Suite**: Controlled, reproducible SVG output tests for all endpoints, with results and reports saved to `/tests/results`.
- **📱 Responsive & Accessible**: Modern React frontend with CSS modules, responsive SVGs, and accessible design.
- **🚀 Easy Deployment**: Pre-configured for Vercel, Neon DB, and local development with `.env.example` and robust error handling.
- **🔗 Direct API Access**: RESTful endpoints for direct SVG generation and easy embedding in Markdown/HTML.
- **🛠️ Extensible Architecture**: Modular backend/frontend for easy addition of new stat types or customizations.

## 🚀 Live Demo

Visit the live demo: [GitHub Stats Animator](https://github-stats-animator.vercel.app)

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
Generate a customizable account statistics card.

**Parameters:**
- `theme` - `light` | `dark` (default: `dark`)
- `icon` - `user` | `github` | `streak` | `user+github` | `user+streak` | `github+streak` (rotating combos supported)
- `animation_time` - Icon rotation duration in seconds (default: `8`)
- `slot1-5` - Statistics to display: `stars`, `commits_total`, `commits_current_year`, `commits_6_months`, `pull_requests`, `code_reviews`, `issues`, `external_contributions`, `streak`

### `/api/top-languages`
Generate a fully animated, responsive top languages bar chart.

**Parameters:**
- `theme` - `light` | `dark` (default: `dark`)
- `languages_count` - Number of languages to show (default: `5`, max: `20`)
- `decimal_places` - Decimal places for percentages (default: `1`, max: `5`)
- `count_other_languages` - Include "Other" category (default: `false`)
- `exclude_languages` - Comma-separated list of languages to exclude
- `width` - Chart width in px (default: `400`, min: `200`, max: `1000`)
- `height` - Chart height in px (default: `300`, min: `150`, max: `800`)

### `/api/contributions-graph`
Generate an animated contributions graph with custom text overlay.

**Parameters:**
- `theme` - `light` | `dark` (default: `dark`)
- `text` - Text to animate over the graph (default: `ADBREEKER`)
- `line_color` - Animation line color (default: `#ff8c00`)
- `line_alpha` - Line transparency 0-1 (default: `0.7`)
- `square_size` - Size of contribution squares (default: `11`, min: `1`, max: `50`)
- `animation_time` - Animation duration in seconds (default: `8.0`)
- `pause_time` - Pause between animations in seconds (default: `0.0`)

### `/api/views-counter`
Animated slot-machine style SVG counter for profile views.

**Parameters:**
- `theme` - `light` | `dark` (default: `dark`)
- `animated` - `true` | `false` (default: `true`)


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
| `NEON_DATABASE_URL` | Neon/Postgres DB URL for persistent views counter | ❌ | `postgres://...` |
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


This project was initially inspired by [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats), but is a complete rewrite with a modern stack and many new features:

- **Animated contributions graphs** with custom pixel font overlays and multi-phase animation
- **Interactive React frontend** for real-time configuration, preview, and SVG download
- **Modern technology stack**: React 19, Vite, Python 3.11+, async GraphQL, and Postgres/Neon DB
- **Advanced SVGs**: Animated bar charts, slot-machine counters, rotating icons, and more
- **Robust testing**: Controlled, reproducible SVG output tests for all endpoints
- **Extensible and modular**: Easy to add new stat types or customize both backend and frontend

The goal: a more customizable, feature-rich, and modern alternative with beautiful animated visuals, robust API, and a delightful user/developer experience.

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
