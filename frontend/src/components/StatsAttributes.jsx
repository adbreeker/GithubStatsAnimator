import { useState, useEffect, useRef } from 'react';
import styles from '../styles/statsAttributes.module.css';

const StatsAttributes = ({ selectedStatsType, config, onConfigChange }) => {
  const [excludedLanguages, setExcludedLanguages] = useState(config.exclude_languages || []);
  const [showLanguageDropdown, setShowLanguageDropdown] = useState(false);
  const [dropdownPosition, setDropdownPosition] = useState('down');
  const dropdownRef = useRef(null);

  // Sync excludedLanguages with config changes
  useEffect(() => {
    setExcludedLanguages(config.exclude_languages || []);
  }, [config.exclude_languages]);

  // Close dropdown when stats type changes
  useEffect(() => {
    setShowLanguageDropdown(false);
  }, [selectedStatsType]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current) {
        const button = dropdownRef.current.querySelector(`.${styles.addLanguageButton}`);
        const dropdown = dropdownRef.current.querySelector(`.${styles.languageDropdown}`);
        
        // Check if click is outside both button and dropdown
        const isClickOnButton = button && button.contains(event.target);
        const isClickOnDropdown = dropdown && dropdown.contains(event.target);
        
        if (!isClickOnButton && !isClickOnDropdown) {
          setShowLanguageDropdown(false);
        }
      }
    };

    if (showLanguageDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [showLanguageDropdown]);

  // Common options for slots (updated to match API)
  const slotOptions = [
    'none',
    'stars',
    'commits_total',
    'commits_current_year',
    'pull_requests',
    'code_reviews',
    'issues',
    'external_contributions'
  ];

  const iconOptions = [
    'user',
    'github',
    'streak',
    'user+github',
    'user+streak',
    'github+streak'
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
    event.preventDefault();
    event.stopPropagation();
    
    if (!showLanguageDropdown) {
      // Calculate if dropdown should go up or down
      const button = event.currentTarget;
      const buttonRect = button.getBoundingClientRect();
      const viewportHeight = window.innerHeight;
      const dropdownHeight = 200; // max-height from CSS
      const spaceBelow = viewportHeight - buttonRect.bottom;
      const spaceAbove = buttonRect.top;
      
      // If there's not enough space below and there's more space above, position upward
      if (spaceBelow < dropdownHeight && spaceAbove > spaceBelow) {
        setDropdownPosition('up');
      } else {
        setDropdownPosition('down');
      }
    }
    
    setShowLanguageDropdown(prev => !prev);
  };

  const addExcludedLanguage = (language) => {
    if (!excludedLanguages.includes(language)) {
      const newExcluded = [...excludedLanguages, language];
      setExcludedLanguages(newExcluded);
      handleConfigUpdate('exclude_languages', newExcluded);
    }
    setShowLanguageDropdown(false);
  };

  const removeExcludedLanguage = (language) => {
    const newExcluded = excludedLanguages.filter(lang => lang !== language);
    setExcludedLanguages(newExcluded);
    handleConfigUpdate('exclude_languages', newExcluded);
  };

  // Custom NumberInput component
  const NumberInput = ({ value, onChange, min, max, step, ...props }) => {
    const handleIncrement = () => {
      const currentValue = parseFloat(value) || 0;
      const stepValue = parseFloat(step) || 1;
      const newValue = Math.min(currentValue + stepValue, max || Infinity);
      const formattedValue = formatNumberValue(newValue, step);
      onChange({ target: { value: formattedValue } });
    };

    const handleDecrement = () => {
      const currentValue = parseFloat(value) || 0;
      const stepValue = parseFloat(step) || 1;
      const newValue = Math.max(currentValue - stepValue, min || -Infinity);
      const formattedValue = formatNumberValue(newValue, step);
      onChange({ target: { value: formattedValue } });
    };

    const handleInputChange = (e) => {
      const inputValue = e.target.value;
      // Allow the user to type freely, but format on blur
      onChange(e);
    };

    const handleBlur = (e) => {
      const inputValue = parseFloat(e.target.value);
      if (!isNaN(inputValue)) {
        const formattedValue = formatNumberValue(inputValue, step);
        onChange({ target: { value: formattedValue } });
      }
    };

    const formatNumberValue = (value, step) => {
      const stepStr = step ? step.toString() : '1';
      const decimalPlaces = stepStr.includes('.') ? stepStr.split('.')[1].length : 0;
      return parseFloat(value.toFixed(decimalPlaces)).toString();
    };

    return (
      <div className={styles.numberInputContainer}>
        <button
          type="button"
          className={`${styles.numberInputButton} ${styles.decrement}`}
          onClick={handleDecrement}
        />
        <input
          type="number"
          className={styles.numberInput}
          value={value}
          onChange={handleInputChange}
          onBlur={handleBlur}
          min={min}
          max={max}
          step={step}
          {...props}
        />
        <button
          type="button"
          className={`${styles.numberInputButton} ${styles.increment}`}
          onClick={handleIncrement}
        />
      </div>
    );
  };

  // ACCOUNT GENERAL ----------------------------------------------------------------------------------------------------------------- ACCOUNT GENERAL
  const renderAccountGeneralConfig = () => (
    <div className={styles.configSection}>
      <h4 className={styles.sectionTitle}>Account General Configuration</h4>
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

      {/* Icon */}
      <div className={styles.configItem}>
        <label className={styles.label}>Icon:</label>
        <select
          className={styles.select}
          value={config.icon || 'user'}
          onChange={(e) => handleConfigUpdate('icon', e.target.value)}
        >
          {iconOptions.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
      </div>

      {/* Animation Time - only show for multi-icons */}
      {(config.icon || 'user').includes('+') && (
        <div className={styles.configItem}>
          <label className={styles.label}>Animation Time (seconds):</label>
          <NumberInput
            value={config.animation_time || 8}
            onChange={(e) => handleConfigUpdate('animation_time', parseFloat(e.target.value))}
            min={1}
            max={30}
            step={0.1}
            className={styles.numberInput}
          />
        </div>
      )}

      {/* Slots 1-5 */}
      {[1, 2, 3, 4, 5].map((slotNum) => (
        <div key={slotNum} className={styles.configItem}>
          <label className={styles.label}>Slot {slotNum}:</label>
          <select
            className={styles.select}
            value={config.slots?.[slotNum - 1] || (slotNum === 1 ? 'stars' : slotNum === 2 ? 'commits_total' : slotNum === 3 ? 'commits_current_year' : slotNum === 4 ? 'pull_requests' : 'issues')}
            onChange={(e) => handleSlotUpdate(slotNum - 1, e.target.value)}
          >
            {slotOptions.map(option => (
              <option key={option} value={option}>{option.replace(/_/g, ' ')}</option>
            ))}
          </select>
        </div>
      ))}
    </div>
  );

  // TOP LANGUAGES ----------------------------------------------------------------------------------------------------------------- TOP LANGUAGES
  const renderTopLanguagesConfig = () => (
    <div className={styles.configSection}>
      <h4 className={styles.sectionTitle}>Top Languages Configuration</h4>
      
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
      
      {/* Languages count slider */}
      <div className={styles.configItem}>
        <label className={styles.label}>Languages Count: {config.languages_count || 5}</label>
        <input
          type="range"
          className={styles.slider}
          min="1"
          max="20"
          value={config.languages_count || 5}
          onChange={(e) => handleConfigUpdate('languages_count', parseInt(e.target.value))}
        />
      </div>

      {/* Decimal places slider */}
      <div className={styles.configItem}>
        <label className={styles.label}>Decimal Places: {config.decimal_places ?? 1}</label>
        <input
          type="range"
          className={styles.slider}
          min="0"
          max="5"
          value={config.decimal_places ?? 1}
          onChange={(e) => handleConfigUpdate('decimal_places', parseInt(e.target.value))}
        />
      </div>

      {/* Count other checkbox */}
      <div className={styles.configItem}>
        <label className={styles.checkboxLabel}>
          <input
            type="checkbox"
            className={styles.checkbox}
            checked={config.count_other_languages || false}
            onChange={(e) => handleConfigUpdate('count_other_languages', e.target.checked)}
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
                className="removeButton removeButtonSmall"
                onClick={() => removeExcludedLanguage(lang)}
              >
              </button>
            </div>
          ))}
          <div className={styles.addLanguageContainer} ref={dropdownRef}>
            <button
              className={styles.addLanguageButton}
              onClick={handleShowLanguageDropdown}
            >
              + Add Language
            </button>
            {showLanguageDropdown && (
              <div className={`${styles.languageDropdown} ${dropdownPosition === 'up' ? styles.dropdownUp : styles.dropdownDown}`}>
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

      {/* Width */}
      <div className={styles.configItem}>
        <label className={styles.label}>Width: {config.width || 400}px</label>
        <input
          type="range"
          className={styles.slider}
          min="200"
          max="1000"
          value={config.width || 400}
          onChange={(e) => handleConfigUpdate('width', parseInt(e.target.value))}
        />
      </div>

      {/* Height */}
      <div className={styles.configItem}>
        <label className={styles.label}>Height: {config.height || 300}px</label>
        <input
          type="range"
          className={styles.slider}
          min="150"
          max="800"
          value={config.height || 300}
          onChange={(e) => handleConfigUpdate('height', parseInt(e.target.value))}
        />
      </div>
    </div>
  );

  // REPOSITORIES ----------------------------------------------------------------------------------------------------------------- REPOSITORIES
  const renderRepositoriesConfig = () => (
    <div className={styles.configSection}>
      <h4 className={styles.sectionTitle}>Repositories Configuration</h4>
      
      {(config.repositorySlots || [{ type: 'none', link: '' }]).map((slot, index) => (
        <div key={index} className={styles.repositorySlot}>
          <div className={styles.slotHeader}>
            <label className={styles.label}>Slot {index + 1}:</label>
            {index > 0 && (
              <button
                className="removeButton removeButtonSmall"
                onClick={() => removeRepositorySlot(index)}
              >
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

  // CONTRIBUTIONS GRAPH ----------------------------------------------------------------------------------------------------------------- CONTRIBUTIONS GRAPH
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

      {/* Text */}
      <div className={styles.configItem}>
        <label className={styles.label}>Text:</label>
        <input
          type="text"
          className={styles.input}
          placeholder="Text to animate (default: ADBREEKER)"
          value={config.text || ''}
          onChange={(e) => handleConfigUpdate('text', e.target.value)}
        />
      </div>

      {/* Animation time */}
      <div className={styles.configItem}>
        <label className={styles.label}>Animation Time (seconds):</label>
        <NumberInput
          min="0.1"
          step="0.1"
          value={config.animation_time || 8.0}
          onChange={(e) => handleConfigUpdate('animation_time', parseFloat(e.target.value))}
        />
      </div>

      {/* Pause time */}
      <div className={styles.configItem}>
        <label className={styles.label}>Pause Time (seconds):</label>
        <NumberInput
          min="0.0"
          step="0.1"
          value={config.pause_time || 0.0}
          onChange={(e) => handleConfigUpdate('pause_time', parseFloat(e.target.value))}
        />
      </div>

      {/* Line color with alpha */}
      <div className={styles.configItem}>
        <label className={styles.label}>Line Color:</label>
        <div className={styles.colorContainer}>
          <div className={styles.colorRow}>
            <input
              type="color"
              className={styles.colorInput}
              value={config.line_color || '#ff8c00'}
              onChange={(e) => handleConfigUpdate('line_color', e.target.value)}
            />
            <span className={styles.colorValue}>{config.line_color || '#ff8c00'}</span>
          </div>
          <div className={styles.alphaRow}>
            <span className={styles.alphaLabel}>Alpha: {(config.line_alpha ?? 0.7).toFixed(2)}</span>
            <input
              type="range"
              className={styles.slider}
              min="0"
              max="1"
              step="0.01"
              value={config.line_alpha ?? 0.7}
              onInput={(e) => {
                const value = Math.max(0, Math.min(1, parseFloat(e.target.value) || 0));
                handleConfigUpdate('line_alpha', value);
              }}
              onChange={(e) => {
                const value = Math.max(0, Math.min(1, parseFloat(e.target.value) || 0));
                handleConfigUpdate('line_alpha', value);
              }}
            />
          </div>
        </div>
      </div>

      {/* Square size */}
      <div className={styles.configItem}>
        <label className={styles.label}>Square Size: {config.square_size || 11}px</label>
        <input
          type="range"
          className={styles.slider}
          min="1"
          max="50"
          value={config.square_size || 11}
          onChange={(e) => handleConfigUpdate('square_size', parseInt(e.target.value))}
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
