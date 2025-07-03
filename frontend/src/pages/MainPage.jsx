import { useState } from 'react';
import StatsTypesList from '../components/StatsTypesList';
import StatsAttributes from '../components/StatsAttributes';
import StatsPreview from '../components/StatsPreview';
import styles from '../styles/mainPage.module.css';

const MainPage = () => {
  const [selectedStatsType, setSelectedStatsType] = useState('Account General');
  const [config, setConfig] = useState({
    slots: ['none', 'none', 'none', 'none', 'none'],
    icon: 'none'
  });

  const getDefaultConfigForType = (type) => {
    switch (type) {
      case 'Account General':
        return {
          slots: ['none', 'none', 'none', 'none', 'none'],
          icon: 'none'
        };
      case 'Top Languages':
        return {
          languagesCount: 5,
          percentageDecimals: 1,
          countOther: false,
          excludedLanguages: []
        };
      case 'Repositories':
        return {
          repositorySlots: [{ type: 'none', link: '' }]
        };
      case 'Contributions Graph':
        return {
          animationTime: 2.0,
          pauseTime: 1.0,
          linesColor: '#39d353',
          linesAlpha: 1.0,
          text: ''
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
