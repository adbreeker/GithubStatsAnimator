import { useState } from 'react';
import styles from '../styles/statsTypesList.module.css';

const StatsTypesList = ({ selectedType, onTypeSelect }) => {
  const statsTypes = [
    'Account General',
    'Top Languages',
    'Repositories',
    'Contributions Graph'
  ];

  return (
    <div className={styles.statsTypesList}>
      <h2 className={styles.title}>Stats Types</h2>
      <div className={styles.typesList}>
        {statsTypes.map((type) => (
          <button
            key={type}
            className={`${styles.typeButton} ${type === 'Repositories' ? styles.disabled : ''} ${selectedType === type ? styles.active : ''}`}
            onClick={type === 'Repositories' ? undefined : () => onTypeSelect(type)}
          >
            {type}
          </button>
        ))}
      </div>
    </div>
  );
};

export default StatsTypesList;
