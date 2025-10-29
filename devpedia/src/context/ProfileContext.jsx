import React, { createContext, useContext, useReducer } from 'react';
import { fetchUser } from '../services/githubService';

const ProfileContext = createContext();

export const useProfile = () => useContext(ProfileContext);

const initialState = {
    user: null,
    isLoading: false,
    error: null,
};

const profileReducer = (state, action) => {
    switch (action.type) {
        case 'FETCH_START':
            return { ...state, isLoading: true, error: null, user: null };
        case 'FETCH_SUCCESS':
            return { ...state, isLoading: false, user: action.payload };
        case 'FETCH_ERROR':
            return { ...state, isLoading: false, error: action.payload };
        case 'RESET':
            return initialState;
        default:
            return state;
    }
};

export const ProfileProvider = ({ children }) => {
    const [state, dispatch] = useReducer(profileReducer, initialState);

    const getUser = async (username) => {
        dispatch({ type: 'FETCH_START' });
        try {
            const userData = await fetchUser(username);
            dispatch({ type: 'FETCH_SUCCESS', payload: userData });
        } catch (error) {
            dispatch({ type: 'FETCH_ERROR', payload: error.message });
        }
    };
    
    const resetProfile = () => {
        dispatch({ type: 'RESET' });
    };

    return (
        <ProfileContext.Provider value={{ ...state, getUser, resetProfile }}>
            {children}
        </ProfileContext.Provider>
    );
};
