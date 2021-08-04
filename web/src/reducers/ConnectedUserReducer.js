export const LOGIN = "CONNECTED_USER_REDUCER/LOGIN";
export const LOGOUT=  "CONNECTED_USER_REDUCER/LOGOUT";


// Initial
const initialState = {
    userName: "",
    email: "",
    isAdmin: false,
    maximumVolume: -1
}

// Events
/*
 * TODO login to server
 * 서버 API를 연결할 경우
 * 모든 함수를 ASYNC 처리하고 axios 옆에 await 추가
*/
export const userLogin = (user, pswd) => {
    // Connect From API Server For check login data

    // Test Case
    return {
        type: LOGIN,
        data: {
            userName: "admin",
            email: "seokbong60@gmail.com",
            isAdmin: true,
            maximumVolume: 100
        }
    }
}
export const userLogout = () => {
    // Connect From api server for logout

    return {
        type: LOGOUT,
        data: {
            userName: "",
            email: "",
            isAdmin: false,
            maximumVolume: -1
        }
    }
}

// Reducmer
export const ConnectedUserReducer = (state = initialState, action) => {
    switch(action.type) {
        case LOGIN: case LOGOUT:
            return {
                userName: action.data.userName,
                email: action.data.email,
                isAdmin: action.data.isAdmin,
                maximumVolume: action.data.maximumVolume
            }
        default:
            return state;
    }
}