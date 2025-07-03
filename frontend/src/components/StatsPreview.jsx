import { useEffect, useState } from 'react';
import styles from '../styles/statsPreview.module.css';

const StatsPreview = ({ selectedStatsType, config }) => {
  const [isLoading, setIsLoading] = useState(false);

  // TODO: This will be connected to backend API later
  // For now, just showing a placeholder with the selected configuration
  
  const generatePreview = () => {
    setIsLoading(true);
    
    // Simulate API call delay
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  };

  useEffect(() => {
    if (config && Object.keys(config).length > 0) {
      generatePreview();
    }
  }, [selectedStatsType, config]);

  const hasConfiguration = () => {
    switch (selectedStatsType) {
      case 'Account General':
        return config.slots?.some(slot => slot !== 'none') || config.icon !== 'none';
      case 'Top Languages':
        return config.languagesCount > 0 || config.excludedLanguages?.length > 0;
      case 'Repositories':
        return config.repositorySlots?.some(slot => slot.type !== 'none');
      case 'Contributions Graph':
        return config.animationTime > 0 || config.text !== '';
      default:
        return false;
    }
  };

  const renderAccountGeneralPreview = () => {
    const activeSlots = config.slots?.filter(slot => slot !== 'none') || [];
    const hasIcon = config.icon !== 'none';

    return (
      <div className={styles.mockProfile}>
        <div className={styles.mockAvatar}></div>
        <div className={styles.mockInfo}>
          <div className={styles.mockUsername}>username</div>
          <div className={styles.mockStats}>
            {activeSlots.map((slot, index) => (
              <span key={index}>� {slot}: 123</span>
            ))}
            {hasIcon && <span>� {config.icon}</span>}
          </div>
        </div>
      </div>
    );
  };

  const renderTopLanguagesPreview = () => {
    const languages = ['JavaScript', 'Python', 'TypeScript', 'Java', 'C++'];
    const displayCount = Math.min(config.languagesCount || 5, languages.length);
    const decimals = config.percentageDecimals || 1;

    return (
      <div className={styles.mockLanguages}>
        <div className={styles.mockLangBar} style={{background: 'linear-gradient(90deg, #f1e05a 40%, #563d7c 30%, #e34c26 30%)'}}></div>
        <div className={styles.mockLangList}>
          {languages.slice(0, displayCount).map((lang, index) => {
            const percentage = (40 - index * 8).toFixed(decimals);
            return <span key={lang}>{lang} {percentage}%</span>;
          })}
          {config.countOther && <span>Other 10.{decimals > 0 ? '0'.repeat(decimals) : ''}%</span>}
          {config.excludedLanguages?.length > 0 && (
            <div className={styles.excludedNote}>
              Excluded: {config.excludedLanguages.join(', ')}
            </div>
          )}
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
      const color = config.linesColor || '#39d353';
      const alpha = config.linesAlpha !== undefined ? config.linesAlpha : 1.0;
      
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
                opacity: Math.random() * 0.6 + 0.4 // Random opacity for visual variety
              }}
            ></div>
          ))}
        </div>
        {config.text && (
          <div className={styles.mockText}>{config.text}</div>
        )}
        <div className={styles.mockAnimationInfo}>
          Animation: {config.animationTime || 2}s | Pause: {config.pauseTime || 1}s
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
      case 'Repositories':
        return renderRepositoriesPreview();
      case 'Contributions Graph':
        return renderContributionsGraphPreview();
      default:
        return <div className={styles.mockDefault}>Preview will appear here</div>;
    }
  };

  return (
    <div className={styles.previewContainer}>
      <div className={styles.header}>
        <h3 className={styles.title}>Stats Preview</h3>
        <div className={styles.configInfo}>
          <span className={styles.statsType}>{selectedStatsType}</span>
          <span className={styles.configStatus}>
            {hasConfiguration() ? 'Configured' : 'Not configured'}
          </span>
        </div>
      </div>

      <div className={styles.previewArea}>
        {isLoading ? (
          <div className={styles.loadingState}>
            <div className={styles.spinner}></div>
            <span>Generating preview...</span>
          </div>
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

      {/* TODO: Connect to backend API */}
      {/* 
      Future implementation:
      - Send selectedStatsType and config to backend
      - Receive generated stats visualization
      - Display real GitHub stats with animation
      - Add export options (PNG, SVG, GIF)
      */}
    </div>
  );
};

export default StatsPreview;
