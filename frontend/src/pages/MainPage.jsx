import { useState } from 'react';
import StatsTypesList from '../components/StatsTypesList';
import StatsAttributes from '../components/StatsAttributes';
import StatsPreview from '../components/StatsPreview';
import styles from '../styles/mainPage.module.css';

const MainPage = () => {
  const [selectedStatsType, setSelectedStatsType] = useState('Account General');
  const [config, setConfig] = useState({
    theme: 'dark',
    slots: ['stars', 'commits_total', 'commits_current_year', 'pull_requests', 'issues'],
    icon: 'user',
    animation_time: 8
  });

  const getDefaultConfigForType = (type) => {
    switch (type) {
      case 'Account General':
        return {
          theme: 'dark',
          slots: ['stars', 'commits_total', 'commits_current_year', 'pull_requests', 'issues'],
          icon: 'user',
          animation_time: 8
        };
      case 'Top Languages':
        return {
          theme: 'dark',
          languages_count: 5,
          decimal_places: 1,
          count_other_languages: false,
          exclude_languages: [],
          width: 400,
          height: 300
        };
      case 'Repositories':
        return {
          repositorySlots: [{ type: 'none', link: '' }]
        };
      case 'Contributions Graph':
        return {
          theme: 'dark',
          text: 'ADBREEKER',
          animation_time: 8.0,
          pause_time: 0.0,
          line_color: '#ff8c00',
          line_alpha: 0.7,
          square_size: 11
        };
      case 'Views Counter':
        return {
          theme: 'dark',
          animated: true
        };
      default:
        return {};
    }
  };

  const handleTypeSelect = (type) => {
    setSelectedStatsType(type);
    setConfig(getDefaultConfigForType(type));
  };

  const handleConfigChange = (newConfig) => {
    setConfig(newConfig);
  };

  return (
    <div className={styles.mainPage}>
      {/* Header with Stats Type Selection */}
      <header className={styles.header}>
        <h1 className={styles.appTitle}>GitHub Stats Animator</h1>
        <StatsTypesList 
          selectedType={selectedStatsType}
          onTypeSelect={handleTypeSelect}
        />
      </header>

      {/* Main Content Area */}
      <main className={styles.mainContent}>
        {/* Left Panel - Configuration */}
        <aside className={styles.leftPanel}>
          <StatsAttributes
            selectedStatsType={selectedStatsType}
            config={config}
            onConfigChange={handleConfigChange}
          />
        </aside>

        {/* Vertical Divider */}
        <div className={styles.divider}></div>

        {/* Right Panel - Preview */}
        <section className={styles.rightPanel}>
          <StatsPreview
            selectedStatsType={selectedStatsType}
            config={config}
          />
        </section>
      </main>
    </div>
  );
};

export default MainPage;
