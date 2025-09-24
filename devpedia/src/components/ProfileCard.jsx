import React from 'react';
import { useFavorites } from '../context/FavoritesContext';
import styles from './ProfileCard.module.css';

const ProfileCard = ({ user }) => {
    const { addFavorite, removeFavorite, isFavorite } = useFavorites();
    const isFav = isFavorite(user.id);

    const handleFavoriteClick = () => {
        if (isFav) {
            removeFavorite(user.id);
        } else {
            addFavorite(user);
        }
    };

    return (
        <div className={styles.card}>
            <img src={user.avatar_url} alt={`Avatar de ${user.name}`} className={styles.avatar} />
            <h2 className={styles.name}>{user.name}</h2>
            <p className={styles.login}>@{user.login}</p>
            <p className={styles.bio}>{user.bio || 'Sem bio.'}</p>
            <div className={styles.stats}>
                <div>
                    <strong>{user.public_repos}</strong>
                    <span>Repositórios</span>
                </div>
                <div>
                    <strong>{user.followers}</strong>
                    <span>Seguidores</span>
                </div>
            </div>
            <button onClick={handleFavoriteClick} className={`${styles.favButton} ${isFav ? styles.isFav : ''}`}>
                {isFav ? 'Remover dos Favoritos' : 'Salvar nos Favoritos'}
            </button>
        </div>
    );
};

export default ProfileCard;
