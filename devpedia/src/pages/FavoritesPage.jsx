import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useFavorites } from '../context/FavoritesContext';
import { useProfile } from '../context/ProfileContext';
import styles from './FavoritesPage.module.css';

const FavoritesPage = () => {
    const { favorites, removeFavorite } = useFavorites();
    const { getUser } = useProfile();
    const navigate = useNavigate();

    const handleProfileClick = (username) => {
        getUser(username);
        navigate('/');
    };

    if (favorites.length === 0) {
        return (
            <div className={styles.emptyMessage}>
                <h2>Nenhum favorito salvo.</h2>
                <p>Volte para a busca e salve alguns perfis!</p>
            </div>
        );
    }

    return (
        <div className={styles.favoritesContainer}>
            <h1>Seus Favoritos</h1>
            <div className={styles.grid}>
                {favorites.map(user => (
                    <div key={user.id} className={styles.favCard}>
                        <img 
                            src={user.avatar_url} 
                            alt={user.name} 
                            onClick={() => handleProfileClick(user.login)}
                        />
                        <h3 onClick={() => handleProfileClick(user.login)}>{user.name}</h3>
                        <p>@{user.login}</p>
                        <button onClick={() => removeFavorite(user.id)}>Remover</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default FavoritesPage;
