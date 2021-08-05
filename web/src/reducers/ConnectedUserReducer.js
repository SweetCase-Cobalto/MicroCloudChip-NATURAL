// example user image

import usrIcon from '../asset/img/icons/user-icon.svg';

export const LOGIN = "CONNECTED_USER_REDUCER/LOGIN";
export const LOGOUT = "CONNECTED_USER_REDUCER/LOGOUT";

// 유저 정보를 수정한 다음 서버로부터 새로운 정보를 받아야 하는 경우 사용
export const UPDATE_INFO = "CONNECTED_USER_REDUCER/UPDATE_INFO";

// Initial
const initialState = {
    id: "",             // 고유 아이디
    userName: "",       // 유저 이름(아이디)
    email: "",          // 유저 아이디
    isAdmin: false,     // 어드민 여부
    usrImgLink: "",     // 유저 이미지 링크
    usedVolume: -1,     // 사용 용량 (KB 단위)
    maximumType: -1     // 최대 이용 용량 (KB  단위)
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
            id: "abcdefg",
            userName: "admin",
            email: "seokbong60@gmail.com",
            isAdmin: true,
            maximumVolume: 100,
            usrImgLink: usrIcon,
            usedVolume: 34
        }
    }
}
export const userLogout = () => {
    // Connect From api server for logout

    return {
        type: LOGOUT,
        data: {
            id: "",
            userName: "",
            email: "",
            isAdmin: false,
            maximumVolume: -1,
            usrImgLink: usrIcon,
            usedVolume: -1
        }
    }
}
// 유저 데이터 수정
export const updateMyInfo = (userName, localUsrImgLink, password) => {
    // Connect With Server

    let _localUsrImgLink = localUsrImgLink == "" ? usrIcon : localUsrImgLink;

    return {
        type: UPDATE_INFO,
        data: {
            userName: userName,
            usrImgLink: _localUsrImgLink
        }
    }
}

// Reducer
export const ConnectedUserReducer = (state = initialState, action) => {
    switch(action.type) {
        case LOGIN: case LOGOUT:
            return {
                userName: action.data.userName,
                email: action.data.email,
                isAdmin: action.data.isAdmin,
                maximumVolume: action.data.maximumVolume,
                usedVolume: action.data.usedVolume,
                usrImgLink: action.data.usrImgLink,
                id: action.data.id
            }
        case UPDATE_INFO:
            return {
                ...state,
                userName: action.data.userName,
                usrImgLink: action.data.usrImgLink,
            }
        default:
            return state;
    }
}