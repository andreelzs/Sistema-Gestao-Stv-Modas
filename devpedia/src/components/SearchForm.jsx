import React, { useState } from 'react';
import { useProfile } from '../context/ProfileContext';
import styles from './SearchForm.module.css';

const SearchForm = () => {
    const [username, setUsername] = useState('');
    const { getUser } = useProfile();

    const handleSubmit = (e) => {
        e.preventDefault();
        if (username.trim()) {
            getUser(username.trim());
        }
    };

    return (
        <form onSubmit={handleSubmit} className={styles.searchForm}>
            <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Digite um usuário do GitHub"
                className={styles.searchInput}
            />
            <button type="submit" className={styles.searchButton}>Buscar</button>
        </form>
    );
};

export default SearchForm;
