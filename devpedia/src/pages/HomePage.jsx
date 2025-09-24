import React from 'react';
import { useProfile } from '../context/ProfileContext';
import SearchForm from '../components/SearchForm';
import ProfileCard from '../components/ProfileCard';
import Loader from '../components/Loader';
import ErrorMessage from '../components/ErrorMessage';
import styles from './HomePage.module.css';

const HomePage = () => {
    const { user, isLoading, error } = useProfile();

    const renderContent = () => {
        if (isLoading) {
            return <Loader />;
        }
        if (error) {
            return <ErrorMessage message={error} />;
        }
        if (user) {
            return <ProfileCard user={user} />;
        }
        return (
            <div className={styles.welcomeMessage}>
                <h2>Bem-vindo ao DevPedia</h2>
                <p>Use a busca para encontrar perfis de desenvolvedores no GitHub.</p>
            </div>
        );
    };

    return (
        <div className={styles.homeContainer}>
            <SearchForm />
            <div className={styles.contentArea}>
                {renderContent()}
            </div>
        </div>
    );
};

export default HomePage;
