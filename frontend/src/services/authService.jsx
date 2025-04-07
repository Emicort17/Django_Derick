import axios from "axios";

//URL de inicio de sesión (JWT)
const API_URL = "http://127.0.0.1:8000"

export const login = async (email, password) => {
    const response = await axios.post(`${API_URL}/users/token/`, {email,password});
    if(response.data.access){
        //Guardar el token en React
        localStorage.setItem("accessToken",response.data.access);
        localStorage.setItem("refreshToken",response.data.refresh);
        localStorage.setItem("user", response.data.user.id)
    }
    return response.data;
}

export const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    window.location.reload(); // Recargar para actualizar estado
}

export const refreshToken = async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) throw new Error('No hay refresh token disponible');
    
    try {
      const response = await axios.post(`${API_URL}/users/token/refresh/`, {
        refresh: refreshToken
      });
      
      localStorage.setItem('accessToken', response.data.access);
      setAuthToken(response.data.access);
      return response.data.access;
    } catch (error) {
      logout();
      throw error;
    }
  };
  
  export const setAuthToken = (token) => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  };
  
  export const isAuthenticated = () => {
    return localStorage.getItem('accessToken') !== null;
  };