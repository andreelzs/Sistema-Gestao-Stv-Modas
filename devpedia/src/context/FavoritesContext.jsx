import React, { createContext, useContext } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';

const FavoritesContext = createContext();

export const useFavorites = () => useContext(FavoritesContext);

export const FavoritesProvider = ({ children }) => {
    const [favorites, setFavorites] = useLocalStorage('favorites', []);

    const addFavorite = (user) => {
        if (!favorites.find(fav => fav.id === user.id)) {
            setFavorites([...favorites, user]);
        }
    };

    const removeFavorite = (userId) => {
        setFavorites(favorites.filter(fav => fav.id !== userId));
    };

    const isFavorite = (userId) => {
        return favorites.some(fav => fav.id === userId);
    };

    return (
        <FavoritesContext.Provider value={{ favorites, addFavorite, removeFavorite, isFavorite }}>
            {children}
        </FavoritesContext.Provider>
    );
};
