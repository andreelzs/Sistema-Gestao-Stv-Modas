import React from 'react';
import styles from './ErrorMessage.module.css';

const ErrorMessage = ({ message }) => {
    return (
        <div className={styles.errorContainer}>
            <p>{message}</p>
        </div>
    );
};

export default ErrorMessage;
