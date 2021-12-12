// ACTIONS
export const UPDATE  = "TOKEN_REDUCER_UPDATE";
export const RESET = "TOKEN_REDUCER_RESET";

const initialState = {
    // id: 고유 static id
    // token: 쿠키 토큰
    id: null, token: null,
}



export const TokenReducer = (state = initialState, action) => {
    switch(action.type) {
        case UPDATE:
            return {
                ...state
            };
        case RESET:
            return {
                ...state
            };
        default:
            return state;
    }
}