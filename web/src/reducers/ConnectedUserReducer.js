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

// Error Codes
import {ErrorCodes} from '../modules/err/errorVariables';

// tool
import {volume_label_to_raw} from '../modules/tool/volume';

// Initial
const initialState = {
    id: "",             // 고유 아이디
    userName: "",       // 유저 이름(아이디)
    email: "",          // 유저 아이디
    isAdmin: false,     // 어드민 여부
    usrImgLink: "",     // 유저 이미지 링크
    usedVolume: -1,     // 사용 용량 (KB 단위)
    maximumVolume: -1,    // 최대 이용 용량 (KB  단위)
    token: "",          // 로그인을 하기 위한 토큰
}
// 로그인이 여부를 확인하는 방법은 usedVolume 또는 maximumType이 -1인 지 확인

// Events
/*
    Error Code 출력 여부에 따라
    에러 페이지도 추가해야 하기 대문에 
    Server API를 직접 추가하지 않고 따로 돌린다.
*/

export const syncUserInfo = (staticId, token) => {

    // 유저 데이터 동기화
    // 나의 유저 상태를 갱신하는 컴포넌트에 추가한다.
    const URL = CONFIG.URL + '/server/user/' + staticId;

    return dispatch => {
        axios.get(URL, {
                headers: { "Set-Cookie": token },
                withCredentials: true,
                crossDomain: true,
            })
            .then((response) => {
                // 데이터 갖고오기
                let data = response.data;

                if(data.code != 0) {
                    // 데이터 갖고오기 실패
                    if(data.code == 4) {
                        // 만료
                        alert("세션이 만료되었습니다.");
                    } else {
                        alert("Server Error");
                    }
                    // 서버 접속 및 데이터를 갱신하는 데 실패했기 때문에
                    // 비어있는 상태로 맨들어 놓는다.
                    return dispatch({
                        type: SYNC_USER_INFO,
                        data: initialState
                    })
                } else {
                    // 송신 성공
                    
                    // Volume Types
                    let capacityVolume = volume_label_to_raw(
                        data['user-info']['volume-type']['type'],
                        data['user-info']['volume-type']['value']
                    )
                    let usedVolume = volume_label_to_raw(
                        data['used-volume']['type'],
                        data['used-volume']['value']
                    )
                    return dispatch({
                        type: SYNC_USER_INFO,
                        data: {
                            id: staticId,
                            userName: data['user-info'].name,
                            email: data['user-info'].email,
                            isAdmin: data['user-info']['is-admin'],
                            maximumVolume: capacityVolume,
                            usedVolume: usedVolume,
                            usrImgLink: usrIcon,
                            token: token
                        }
                    })
                }
            })
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
            usedVolume: -1,
            token: "",
        }
    }
}

export const userLogin = (email, pswd) => {

    const formData = new FormData();
    formData.append("email", email);
    formData.append("pswd", pswd);

    // 서버 요청
    let URL = CONFIG.URL + "/server/user/login";

    return dispatch => {axios.post(URL, formData, { withCredentials: true }).then((response) => {
    
        let data = response.data;
        if(data.code == ErrorCodes.ERR_LOGIN_FAILED) {
            // 로그인 실패
            alert("Login Failed");
            return dispatch({
                
                type: LOGIN,
                data: {
                    id: "",
                    userName: "",
                    email: "",
                    isAdmin: false,
                    maximumVolume: -1,
                    usrImgLink: usrIcon,
                    usedVolume: -1,
                    token: "",
                }
            })
        } else if(data.code == 0) {
            // 로그인 성공
            let raw_maximum_volume = volume_label_to_raw(
                data.data['volume-type']['value']['unit'],
                data.data['volume-type']['value']['volume']
            )

            return dispatch({
                type: LOGIN,
                data: {
                    id: data.data['static-id'],
                    userName: data.data['name'],
                    email: data.data['email'],
                    isAdmin: data.data['is-admin'],
                    maximumVolume: raw_maximum_volume,
                    usrImgLink: usrIcon,
                    usedVolume: -1,
                    token: data.data['token']
                }
            })
        }
    })}
}
export const userLogout = (token) => {

    let URL = CONFIG.URL + '/server/user/logout';

    return dispatch => {
        axios.get(URL, {
            headers: { "Set-Cookie": token },
            withCredentials: true,
            crossDomain: true,
        }).then((response) => {
            let data = response.data;
            if(data.code == 0) {
                // 로그아웃 성공
                return dispatch({
                    type: LOGIN,
                    data: {
                        id: "",
                        userName: "",
                        email: "",
                        isAdmin: false,
                        maximumVolume: -1,
                        usrImgLink: usrIcon,
                        usedVolume: -1,
                        token: ""
                    }
                })
            }
        })
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
                id: action.data.id,
                token: action.data.token
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
                id: action.data.id,
                token: action.data.token,
                usrImgLink: action.data.usrImgLink
            }
        default:
            return state;
    }
}