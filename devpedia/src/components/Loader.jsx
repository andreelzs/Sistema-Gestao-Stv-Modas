import React from 'react';
import styles from './Loader.module.css';

const Loader = () => {
    return (
        <div className={styles.loaderContainer}>
            <div className={styles.loader}></div>
            <p>Carregando...</p>
        </div>
    );
};

export default Loader;
