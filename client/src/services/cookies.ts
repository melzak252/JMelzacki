import Cookies from 'js-cookie';

export const setTokenCookie = (token: string) => {
  Cookies.set('access_token', token);
};

export const getTokenCookie = () => {
  return Cookies.get('access_token');
};

export const removeTokenCookie = () => {
  Cookies.remove('access_token');
};