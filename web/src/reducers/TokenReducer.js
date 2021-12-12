// ACTIONS
const UPDATE  = "TOKEN_REDUCER_UPDATE";
const RESET = "TOKEN_REDUCER_RESET";

const initialState = {
    // id: 고유 static id
    // token: 쿠키 토큰
    id: null, token: null,
}

export const updateTokenInReducer = (_id, _token) => {
    return {
    "type": UPDATE,
    "data": {id: _id, token: _token}
}}
export const resetTokenReducer = () => ({
    "type": RESET
})

export const TokenReducer = (state = initialState, action) => {
    switch(action.type) {
        case UPDATE:
            return { ...state, id: action.data['id'], token: action.data['token'] };
        case RESET:
            return { ...state, id: null, token: null };
        default:
            return state;
    }
}