let API_SERVER_VAL = '';

switch (process.env.NODE_ENV) {
    case 'development':
        API_SERVER_VAL = 'http://localhost:8000/api/';
        break;
    case 'production':
        API_SERVER_VAL = process.env.REACT_APP_API_SERVER;
        break;
    default:
        API_SERVER_VAL = 'http://localhost:8000/api/';
        break;
}

export const API_SERVER = API_SERVER_VAL;
export const API_SERVER_MEDIA = API_SERVER_VAL + 'media/';