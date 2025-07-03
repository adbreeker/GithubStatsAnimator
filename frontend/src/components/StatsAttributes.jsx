import { useState } from 'react';
import styles from '../styles/statsAttributes.module.css';

const StatsAttributes = ({ selectedStatsType, config, onConfigChange }) => {
  const [excludedLanguages, setExcludedLanguages] = useState(config.excludedLanguages || []);
  const [showLanguageDropdown, setShowLanguageDropdown] = useState(false);

  // Common options for slots
  const slotOptions = [
    'none',
    'total stars',
    'total commits',
    'commits current year',
    'total pull requests',
    'total issues',
    'external contributions'
  ];

  const iconOptions = [
    'none',
    'current streak',
    'github logo',
    'grade'
  ];

  const repositorySlotOptions = [
    'most contributions repository',
    'recent top repository',
    'favorite repository',
    'selected repository'
  ];

  // Common programming languages
  const programmingLanguages = [
    'Ada', 'Angular', 'Assembly', 'Batch', 'C', 'C#', 'C++', 'CSS', 'COBOL', 'Clojure', 
    'Common Lisp', 'Crystal', 'D', 'Dart', 'Delphi', 'Deno', 'Elixir', 'Emacs Lisp', 
    'Erlang', 'F#', 'Fortran', 'GLSL', 'Go', 'GraphQL', 'HLSL', 'HTML', 'Haskell', 
    'Java', 'JavaScript', 'Julia', 'Kotlin', 'Less', 'Lua', 'MATLAB', 'MongoDB', 'MySQL', 
    'Nim', 'Node.js', 'OCaml', 'PHP', 'Pascal', 'Perl', 'PostgreSQL', 'PowerShell', 
    'Python', 'R', 'React', 'Redis', 'Ruby', 'Rust', 'SCSS', 'SQL', 'Scala', 'Scheme', 
    'ShaderLab', 'Shell', 'Stylus', 'Svelte', 'Swift', 'Tcl', 'TypeScript', 'VHDL', 
    'Verilog', 'Vim script', 'Vue', 'Zig'
  ];

  const handleConfigUpdate = (key, value) => {
    const newConfig = { ...config, [key]: value };
    onConfigChange(newConfig);
  };

  const handleSlotUpdate = (slotIndex, value) => {
    const slots = [...(config.slots || Array(5).fill('none'))];
    slots[slotIndex] = value;
    handleConfigUpdate('slots', slots);
  };

  const handleRepositorySlotUpdate = (slotIndex, field, value) => {
    const repoSlots = [...(config.repositorySlots || [{ type: 'none', link: '' }])];
    if (!repoSlots[slotIndex]) {
      repoSlots[slotIndex] = { type: 'none', link: '' };
    }
    repoSlots[slotIndex] = { ...repoSlots[slotIndex], [field]: value };
    handleConfigUpdate('repositorySlots', repoSlots);
  };

  const addRepositorySlot = () => {
    const repoSlots = [...(config.repositorySlots || [])];
    repoSlots.push({ type: 'none', link: '' });
    handleConfigUpdate('repositorySlots', repoSlots);
  };

  const removeRepositorySlot = (index) => {
    const repoSlots = [...(config.repositorySlots || [])];
    repoSlots.splice(index, 1);
    handleConfigUpdate('repositorySlots', repoSlots);
  };

  const handleShowLanguageDropdown = (event) => {
    setShowLanguageDropdown(!showLanguageDropdown);
  };

  const addExcludedLanguage = (language) => {
    if (!excludedLanguages.includes(language)) {
      const newExcluded = [...excludedLanguages, language];
      setExcludedLanguages(newExcluded);
      handleConfigUpdate('excludedLanguages', newExcluded);
    }
    setShowLanguageDropdown(false);
  };

  const removeExcludedLanguage = (language) => {
    const newExcluded = excludedLanguages.filter(lang => lang !== language);
    setExcludedLanguages(newExcluded);
    handleConfigUpdate('excludedLanguages', newExcluded);
  };

  const renderAccountGeneralConfig = () => (
    <div className={styles.configSection}>
      <h4 className={styles.sectionTitle}>Account General Configuration</h4>
      
      {/* Icon */}
      <div className={styles.configItem}>
        <label className={styles.label}>Icon:</label>
        <select
          className={styles.select}
          value={config.icon || 'none'}
          onChange={(e) => handleConfigUpdate('icon', e.target.value)}
        >
          {iconOptions.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
      </div>

      {/* Slots 1-5 */}
      {[1, 2, 3, 4, 5].map((slotNum) => (
        <div key={slotNum} className={styles.configItem}>
          <label className={styles.label}>Slot {slotNum}:</label>
          <select
            className={styles.select}
            value={config.slots?.[slotNum - 1] || 'none'}
            onChange={(e) => handleSlotUpdate(slotNum - 1, e.target.value)}
          >
            {slotOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </div>
      ))}
    </div>
  );

  const renderTopLanguagesConfig = () => (
    <div className={styles.configSection}>
      <h4 className={styles.sectionTitle}>Top Languages Configuration</h4>
      
      {/* Languages count slider */}
      <div className={styles.configItem}>
        <label className={styles.label}>Languages Count: {config.languagesCount || 5}</label>
        <input
          type="range"
          className={styles.slider}
          min="1"
          max="10"
          value={config.languagesCount || 5}
          onChange={(e) => handleConfigUpdate('languagesCount', parseInt(e.target.value))}
        />
      </div>

      {/* Percentage floating point slider */}
      <div className={styles.configItem}>
        <label className={styles.label}>Percentage Decimal Places: {config.percentageDecimals || 1}</label>
        <input
          type="range"
          className={styles.slider}
          min="0"
          max="3"
          value={config.percentageDecimals || 1}
          onChange={(e) => handleConfigUpdate('percentageDecimals', parseInt(e.target.value))}
        />
      </div>

      {/* Count other checkbox */}
      <div className={styles.configItem}>
        <label className={styles.checkboxLabel}>
          <input
            type="checkbox"
            className={styles.checkbox}
            checked={config.countOther || false}
            onChange={(e) => handleConfigUpdate('countOther', e.target.checked)}
          />
          Count Other Languages
        </label>
      </div>

      {/* Exclude languages */}
      <div className={styles.configItem}>
        <label className={styles.label}>Exclude Languages:</label>
        <div className={styles.excludedLanguages}>
          {excludedLanguages.map((lang) => (
            <div key={lang} className={styles.languageTag}>
              <span>{lang}</span>
              <button 
                className={styles.removeTag}
                onClick={() => removeExcludedLanguage(lang)}
              >
                ×
              </button>
            </div>
          ))}
          <div className={styles.addLanguageContainer}>
            <button
              className={styles.addLanguageButton}
              onClick={() => setShowLanguageDropdown(!showLanguageDropdown)}
            >
              + Add Language
            </button>
            {showLanguageDropdown && (
              <div className={styles.languageDropdown}>
                {programmingLanguages
                  .filter(lang => !excludedLanguages.includes(lang))
                  .map((lang) => (
                    <button
                      key={lang}
                      className={styles.languageOption}
                      onClick={() => addExcludedLanguage(lang)}
                    >
                      {lang}
                    </button>
                  ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  const renderRepositoriesConfig = () => (
    <div className={styles.configSection}>
      <h4 className={styles.sectionTitle}>Repositories Configuration</h4>
      
      {(config.repositorySlots || [{ type: 'none', link: '' }]).map((slot, index) => (
        <div key={index} className={styles.repositorySlot}>
          <div className={styles.slotHeader}>
            <label className={styles.label}>Slot {index + 1}:</label>
            {index > 0 && (
              <button
                className={styles.removeSlotButton}
                onClick={() => removeRepositorySlot(index)}
              >
                ×
              </button>
            )}
          </div>
          
          <select
            className={styles.select}
            value={slot.type || 'none'}
            onChange={(e) => handleRepositorySlotUpdate(index, 'type', e.target.value)}
          >
            <option value="none">none</option>
            {repositorySlotOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>

          {(slot.type === 'favorite repository' || slot.type === 'selected repository') && (
            <input
              type="text"
              className={styles.input}
              placeholder="Repository link (e.g., username/repository-name)"
              value={slot.link || ''}
              onChange={(e) => handleRepositorySlotUpdate(index, 'link', e.target.value)}
            />
          )}
        </div>
      ))}

      <button
        className={styles.addSlotButton}
        onClick={addRepositorySlot}
      >
        + Add Repository Slot
      </button>
    </div>
  );

  const renderContributionsGraphConfig = () => (
    <div className={styles.configSection}>
      <h4 className={styles.sectionTitle}>Contributions Graph Configuration</h4>
      
      {/* Theme */}
      <div className={styles.configItem}>
        <label className={styles.label}>Theme:</label>
        <div className={styles.themeButtons}>
          <button
            className={`${styles.themeButton} ${(config.theme || 'dark') === 'dark' ? styles.active : ''}`}
            onClick={() => handleConfigUpdate('theme', 'dark')}
          >
            Dark
          </button>
          <button
            className={`${styles.themeButton} ${config.theme === 'light' ? styles.active : ''}`}
            onClick={() => handleConfigUpdate('theme', 'light')}
          >
            Light
          </button>
        </div>
      </div>

      {/* Animation time */}
      <div className={styles.configItem}>
        <label className={styles.label}>Animation Time (seconds):</label>
        <input
          type="number"
          className={styles.numberInput}
          min="0.1"
          step="0.1"
          value={config.animationTime || 2.0}
          onChange={(e) => handleConfigUpdate('animationTime', parseFloat(e.target.value))}
        />
      </div>

      {/* Pause time */}
      <div className={styles.configItem}>
        <label className={styles.label}>Pause Time (seconds):</label>
        <input
          type="number"
          className={styles.numberInput}
          min="0.1"
          step="0.1"
          value={config.pauseTime || 1.0}
          onChange={(e) => handleConfigUpdate('pauseTime', parseFloat(e.target.value))}
        />
      </div>

      {/* Text */}
      <div className={styles.configItem}>
        <label className={styles.label}>Text:</label>
        <input
          type="text"
          className={styles.input}
          placeholder="Enter custom text..."
          value={config.text || ''}
          onChange={(e) => handleConfigUpdate('text', e.target.value)}
        />
      </div>

      {/* Lines color with alpha */}
      <div className={styles.configItem}>
        <label className={styles.label}>Line Color:</label>
        <div className={styles.colorContainer}>
          <div className={styles.colorRow}>
            <input
              type="color"
              className={styles.colorInput}
              value={config.linesColor || '#39d353'}
              onChange={(e) => handleConfigUpdate('linesColor', e.target.value)}
            />
            <span className={styles.colorValue}>{config.linesColor || '#39d353'}</span>
          </div>
          <div className={styles.alphaRow}>
            <span className={styles.alphaLabel}>Alpha: {(config.linesAlpha || 1.0).toFixed(2)}</span>
            <input
              type="range"
              className={styles.slider}
              min="0"
              max="1"
              step="0.01"
              value={config.linesAlpha || 1.0}
              onChange={(e) => handleConfigUpdate('linesAlpha', parseFloat(e.target.value))}
            />
          </div>
        </div>
      </div>

      {/* Square size */}
      <div className={styles.configItem}>
        <label className={styles.label}>Square Size: {config.squareSize || 11}px</label>
        <input
          type="range"
          className={styles.slider}
          min="1"
          max="50"
          value={config.squareSize || 11}
          onChange={(e) => handleConfigUpdate('squareSize', parseInt(e.target.value))}
        />
      </div>
    </div>
  );

  const renderConfigForType = () => {
    switch (selectedStatsType) {
      case 'Account General':
        return renderAccountGeneralConfig();
      case 'Top Languages':
        return renderTopLanguagesConfig();
      case 'Repositories':
        return renderRepositoriesConfig();
      case 'Contributions Graph':
        return renderContributionsGraphConfig();
      default:
        return (
          <div className={styles.emptyState}>
            Select a stats type to configure attributes.
          </div>
        );
    }
  };

  return (
    <div className={styles.attributesPanel}>
      <div className={styles.header}>
        <h3 className={styles.title}>Configuration</h3>
      </div>

      {renderConfigForType()}
    </div>
  );
};

export default StatsAttributes;
