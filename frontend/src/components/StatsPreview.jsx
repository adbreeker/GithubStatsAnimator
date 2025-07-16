import { useEffect, useState, useRef } from 'react';
import styles from '../styles/statsPreview.module.css';

const StatsPreview = ({ selectedStatsType, config }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [svgContent, setSvgContent] = useState(null);
  const [error, setError] = useState(null);

  // Debounce timer ref
  const debounceTimerRef = useRef(null);

  const generatePreview = async () => {
    if (!hasConfiguration()) return;

    setIsLoading(true);
    setError(null);

    try {
      const apiEndpoint = getApiEndpoint();
      const queryParams = buildQueryParams();
      const response = await fetch(`${apiEndpoint}?${queryParams}`);
      if (!response.ok) {
        // Try to extract error message from JSON, fallback to status
        let errorMsg = `HTTP error! status: ${response.status}`;
        try {
          const data = await response.json();
          if (data && data.error) {
            errorMsg = data.error;
          }
        } catch (e) {
          // fallback: keep status message
        }
        throw new Error(errorMsg);
      }
      const svgText = await response.text();
      setSvgContent(svgText);
    } catch (err) {
      console.error('Error fetching SVG:', err);
      setError(err.message);
      setSvgContent(null);
    } finally {
      setIsLoading(false);
    }
  };

  const getApiEndpoint = () => {
    switch (selectedStatsType) {
      case 'Account General':
        return '/api/account-general';
      case 'Top Languages':
        return '/api/top-languages';
      case 'Contributions Graph':
        return '/api/contributions-graph';
      case 'Views Counter':
        return '/api/views-counter';
      default:
        throw new Error(`Unknown stats type: ${selectedStatsType}`);
    }
  };

  const buildQueryParams = () => {
    const params = new URLSearchParams();
    
    switch (selectedStatsType) {
      case 'Account General':
        if (config.theme) params.append('theme', config.theme);
        if (config.icon) params.append('icon', config.icon);
        if ((config.icon || 'user').includes('+') && config.animation_time) {
          params.append('animation_time', config.animation_time);
        }
        if (config.slots) {
          config.slots.forEach((slot, index) => {
            if (slot !== 'none') {
              params.append(`slot${index + 1}`, slot);
            }
          });
        }
        break;
      case 'Top Languages':
        if (config.theme) params.append('theme', config.theme);
        if (config.languages_count) params.append('languages_count', config.languages_count);
        if (config.decimal_places !== undefined) params.append('decimal_places', config.decimal_places);
        if (config.count_other_languages) params.append('count_other_languages', config.count_other_languages);
        if (config.exclude_languages && config.exclude_languages.length > 0) {
          params.append('exclude_languages', config.exclude_languages.join(','));
        }
        if (config.width) params.append('width', config.width);
        if (config.height) params.append('height', config.height);
        break;
      case 'Views Counter':
        if (config.theme) params.append('theme', config.theme);
        if (config.animated !== undefined) params.append('animated', config.animated);
        break;
      case 'Contributions Graph':
        if (config.theme) params.append('theme', config.theme);
        if (config.text) params.append('text', config.text);
        if (config.animation_time) params.append('animation_time', config.animation_time);
        if (config.pause_time) params.append('pause_time', config.pause_time);
        if (config.line_color) params.append('line_color', config.line_color);
        if (config.line_alpha !== undefined) params.append('line_alpha', config.line_alpha);
        if (config.square_size) params.append('square_size', config.square_size);
        break;
    }
    
    return params.toString();
  };

  useEffect(() => {
    // When stats change, set loading immediately
    if (config && Object.keys(config).length > 0 && hasConfiguration()) {
      setIsLoading(true);
    }
    // Debounce preview generation
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    debounceTimerRef.current = setTimeout(() => {
      if (config && Object.keys(config).length > 0 && hasConfiguration()) {
        generatePreview();
      }
    }, 500);
    // Cleanup on unmount
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, [selectedStatsType, config]);

  const hasConfiguration = () => {
    switch (selectedStatsType) {
      case 'Account General':
        return config.slots?.some(slot => slot !== 'none') || config.icon !== 'user';
      case 'Top Languages':
        return config.languages_count > 0 || config.exclude_languages?.length > 0;
      case 'Repositories':
        return config.repositorySlots?.some(slot => slot.type !== 'none');
      case 'Contributions Graph':
        return config.animation_time > 0 || config.text !== '';
      case 'Views Counter':
        return !!config.theme;
      default:
        return false;
    }
  };

  const renderAccountGeneralPreview = () => {
    const activeSlots = config.slots?.filter(slot => slot !== 'none') || [];
    const hasIcon = config.icon !== 'user';

    return (
      <div className={styles.mockProfile}>
        <div className={styles.mockAvatar}></div>
        <div className={styles.mockInfo}>
          <div className={styles.mockUsername}>username</div>
          <div className={styles.mockStats}>
            {activeSlots.map((slot, index) => (
              <span key={index}>🔸 {slot.replace(/_/g, ' ')}: 123</span>
            ))}
            {hasIcon && <span>🔸 {config.icon}</span>}
            <div style={{marginTop: '8px', fontSize: '12px', color: '#888'}}>
              {config.width || 500}×{config.height || 200}px
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderTopLanguagesPreview = () => {
    const languages = ['JavaScript', 'Python', 'TypeScript', 'Java', 'C++'];
    const displayCount = Math.min(config.languages_count || 5, languages.length);
    const decimals = config.decimal_places || 1;

    return (
      <div className={styles.mockLanguages}>
        <div className={styles.mockLangBar} style={{background: 'linear-gradient(90deg, #f1e05a 40%, #563d7c 30%, #e34c26 30%)'}}></div>
        <div className={styles.mockLangList}>
          {languages.slice(0, displayCount).map((lang, index) => {
            const percentage = (40 - index * 8).toFixed(decimals);
            return <span key={lang}>{lang} {percentage}%</span>;
          })}
          {config.count_other_languages && <span>Other 10.{decimals > 0 ? '0'.repeat(decimals) : ''}%</span>}
          {config.exclude_languages?.length > 0 && (
            <div className={styles.excludedNote}>
              Excluded: {config.exclude_languages.join(', ')}
            </div>
          )}
          <div style={{marginTop: '8px', fontSize: '12px', color: '#888'}}>
            {config.width || 400}×{config.height || 300}px
          </div>
        </div>
      </div>
    );
  };

  const renderRepositoriesPreview = () => {
    const activeSlots = config.repositorySlots?.filter(slot => slot.type !== 'none') || [];

    return (
      <div className={styles.mockRepos}>
        {activeSlots.map((slot, index) => (
          <div key={index} className={styles.mockRepo}>
            <div className={styles.mockRepoName}>
              {slot.type === 'selected repository' || slot.type === 'favorite repository' 
                ? slot.link || 'repository-name' 
                : `${slot.type.replace(' repository', '')}-repo`}
            </div>
            <div className={styles.mockRepoDesc}>
              {slot.type} - Repository description...
            </div>
            <div className={styles.mockRepoStats}>⭐ 42 🍴 12 JavaScript</div>
          </div>
        ))}
      </div>
    );
  };

  const renderContributionsGraphPreview = () => {
    const hexToRgba = (hex, alpha) => {
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    };

    const getColor = () => {
      const color = config.line_color || '#ff8c00';
      const alpha = config.line_alpha !== undefined ? config.line_alpha : 0.7;
      
      if (color.startsWith('#')) {
        return hexToRgba(color, alpha);
      } else if (color.startsWith('rgba') || color.startsWith('rgb')) {
        return color;
      }
      return color;
    };

    return (
      <div className={styles.mockContributions}>
        <div className={styles.mockGrid}>
          {Array.from({length: 365}).map((_, i) => (
            <div 
              key={i} 
              className={styles.mockContribDay}
              style={{
                backgroundColor: getColor(),
                opacity: Math.random() * 0.6 + 0.4, // Random opacity for visual variety
                width: `${Math.min(config.square_size || 11, 20)}px`,
                height: `${Math.min(config.square_size || 11, 20)}px`
              }}
            ></div>
          ))}
        </div>
        {config.text && (
          <div className={styles.mockText}>{config.text}</div>
        )}
        <div className={styles.mockAnimationInfo}>
          Animation: {config.animation_time || 8}s | Pause: {config.pause_time || 0}s | Theme: {config.theme || 'dark'}
        </div>
      </div>
    );
  };

  const renderViewsCounterPreview = () => {
    return (
      <div className={styles.mockProfile}>
        <div className={styles.mockAvatar}></div>
        <div className={styles.mockInfo}>
          <div className={styles.mockUsername}>username</div>
          <div className={styles.mockStats}>
            <span>Views Counter</span>
            <div style={{marginTop: '8px', fontSize: '12px', color: '#888'}}>
              Theme: {config.theme || 'dark'} | Animated: {config.animated ? 'Yes' : 'No'}
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderPlaceholderContent = () => {
    switch (selectedStatsType) {
      case 'Account General':
        return renderAccountGeneralPreview();
      case 'Top Languages':
        return renderTopLanguagesPreview();
      case 'Views Counter':
        return renderViewsCounterPreview();
      case 'Repositories':
        return renderRepositoriesPreview();
      case 'Contributions Graph':
        return renderContributionsGraphPreview();
      default:
        return <div className={styles.mockDefault}>Preview will appear here</div>;
    }
  };

  const downloadSVG = () => {
    if (!svgContent) return;
    
    const blob = new Blob([svgContent], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `github-stats-${selectedStatsType.toLowerCase().replace(/\s+/g, '-')}.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const copyApiUrl = () => {
    const apiEndpoint = getApiEndpoint();
    const queryParams = buildQueryParams();
    const fullUrl = `${window.location.origin}${apiEndpoint}?${queryParams}`;
    
    navigator.clipboard.writeText(fullUrl).then(() => {
      // You could add a toast notification here
      console.log('API URL copied to clipboard');
    });
  };

  return (
    <div className={styles.previewContainer}>
      <div className={styles.header}>
        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', width: '100%' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <h3 className={styles.title}>Stats Preview</h3>
            <div className={styles.apiInfo}>
              <span className={styles.badge} style={{ fontSize: '9px', padding: '2px 4px', lineHeight: '1.5' }}>Live Data</span>
              <span style={{ marginLeft: 2, fontSize: '9px', lineHeight: '1.2' }}>Connected to GitHub API</span>
            </div>
          </div>
          <div className={styles.headerActions}>
            <div className={styles.configInfo}>
              <span className={styles.statsType}>{selectedStatsType}</span>
              <span className={styles.configStatus}>
                {hasConfiguration() ? 'Configured' : 'Not configured'}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.previewArea}>
        {isLoading ? (
          <div className={styles.loadingState}>
            <div className={styles.spinner}></div>
            <span>Generating SVG...</span>
          </div>
        ) : error ? (
          <div className={styles.errorState}>
            <div className={styles.errorIcon}>⚠️</div>
            <p>Error generating SVG: {error}</p>
            <button onClick={generatePreview} className={styles.retryButton}>
              Retry
            </button>
          </div>
        ) : svgContent ? (
          <div 
            className={styles.svgContainer}
            dangerouslySetInnerHTML={{ __html: svgContent }}
          />
        ) : hasConfiguration() ? (
          <div className={styles.previewContent}>
            {renderPlaceholderContent()}
          </div>
        ) : (
          <div className={styles.emptyState}>
            <div className={styles.emptyIcon}>📊</div>
            <p>Configure attributes to see preview</p>
          </div>
        )}
      </div>
      {/* API Link at the bottom */}
      <div className={styles.apiBar}>
        <span className={styles.apiLink}>{`${window.location.origin}${getApiEndpoint()}?${buildQueryParams()}`}</span>
      </div>
      {/* Action Buttons below the API bar */}
      <div className={styles.actionButtons} style={{ marginTop: 8 }}>
        <button
          className={styles.actionButton}
          onClick={copyApiUrl}
          type="button"
        >
          Copy URL
        </button>
        <button
          className={styles.actionButton}
          onClick={downloadSVG}
          type="button"
          disabled={!svgContent}
          title={!svgContent ? 'No SVG generated yet' : 'Save as SVG'}
        >
          Save as SVG
        </button>
      </div>
    </div>
  );
};

export default StatsPreview;
