/* 얘는 Admin만 접근해야 한다  */
import usrIcon from '../asset/img/icons/user-icon.svg';
import CONFIG from '../asset/config.json';
import axios from 'axios';

export const UPDATE_USERLIST = "USER_LIST_REDUCER/UPDATE_USER_LIST";

export const updateUserList = (token) => {
    
    // 검색 url
    let URL = `${CONFIG.URL}/server/user/list`;

    
    return dispatch => {
        axios.get(URL, {
            headers: {"Set-Cookie": token},
            withCredentials: true,
            crossDomain: true
        })
        .then((response) => {
            // 통신 성공
            let data = response.data;
            if(data.code == 0) {
                // 정상적인 접근
                const userList = data.data;
                
                // 메인 어드민 인덱스 (삭제하기 위한 인덱스 버퍼)
                let adminIdx = -1

                // 데이터 가공
                for(var i = 0; i < userList.length; i++) {
                    
                    // admin + 관리자 권한 제외
                    if(userList[i].username == 'admin' && userList[i].isAdmin) {
                        adminIdx = i
                        continue;
                    }
                    
                    
                    // 유저 이미지가 없으면 기본 이미지로 대체한다.
                    if(userList[i].userImgLink === null) {
                        userList[i].userImgLink = usrIcon
                    }
                }

                
                return dispatch({
                    type: UPDATE_USERLIST,
                    userList: userList
                })
            } else {
                // 통신 오류
                alert("접근 권한이 없습니다.");
                window.location.relaoad();
            }
        })
    }
};

const initialState = {
    userList: undefined
}
export const UserListReducer = (state = initialState, action) => {
    switch(action.type) {
        case UPDATE_USERLIST:
            return {
                userList: action.userList
            };
        default:
            return state;
    }
};