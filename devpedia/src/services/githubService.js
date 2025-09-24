const API_URL = 'https://api.github.com/users/';

export const fetchUser = async (username) => {
    const response = await fetch(`${API_URL}${username}`);
    
    if (!response.ok) {
        if (response.status === 404) {
            throw new Error('Usuário não encontrado.');
        }
        throw new Error('Ocorreu um erro na busca.');
    }
    
    const data = await response.json();
    return data;
};
