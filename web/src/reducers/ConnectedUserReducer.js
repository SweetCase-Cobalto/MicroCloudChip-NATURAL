// 현재 로그인 되어 있는 유저 정보

import axios from 'axios'
import CONFIG  from '../asset/config.json'

import usrIcon from '../asset/img/icons/user-icon.svg';

export const LOGIN = "CONNECTED_USER_REDUCER/LOGIN";
export const LOGOUT = "CONNECTED_USER_REDUCER/LOGOUT";

// 유저 정보를 수정한 다음 서버로부터 새로운 정보를 받아야 하는 경우 사용
export const UPDATE_INFO = "CONNECTED_USER_REDUCER/UPDATE_INFO";

export const SYNC_USER_INFO = "CONNECTED_USER_REDUCER/SYNC_USER_INFO";
export const RESET_USER_INFO = "CONNECTED_USER_REDUCER/RESET_USER_INFO";

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
// 로그인이 여부를 확인하는 방법은 usedVolume 또는 maximumType이 -1인 지 확인

// Events
/*
    Error Code 출력 여부에 따라
    에러 페이지도 추가해야 하기 대문에 
    Server API를 직접 추가하지 않고 따로 돌린다.
*/

export const syncUserInfo = (req) => {

    // 유저 데이터 동기화
    // 해당 Reducer를 사용하는 매 페이지 마다 이 함수를 사용해야 한다.
    
    return {
        type: SYNC_USER_INFO,
        data: {
            id: req['id'],
            userName: req['userName'],
            email: req['email'],
            isAdmin: req['isAdmin'],
            maximumVolume: req['maximumVolume'],
            usrImgLink: "",
            usedVolume: req['usedVolume']
        }
    }
    
}
export const setUserInfoEmpty = () => {
    
    return {
        type: RESET_USER_INFO,
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

export const userLogin = (email, pswd) => {

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
        case SYNC_USER_INFO: case RESET_USER_INFO:
            return {
                userName: action.data.userName,
                email: action.data.email,
                isAdmin: action.data.isAdmin,
                maximumVolume: action.data.maximumVolume,
                usedVolume: action.data.usedVolume,
                usrImgLink: action.data.usrImgLink,
                id: action.data.id
            }
        default:
            return state;
    }
}