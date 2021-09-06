/* 얘는 Admin만 접근해야 한다  */
import usrIcon from '../asset/img/icons/user-icon.svg';
import CONFIG from '../asset/config.json';

export const UPDATE_USERLIST = "USER_LIST_REDUCER/UPDATE_USER_LIST";

export const updateUserList = (token) => {
    
    // 검색 url
    let URL = `${CONFIG.URL}/server/user`;


    let userList = [
        {
            "username": "user1",
            "user_static_id": "1235rgasdf",
            "userImgLink": usrIcon
        },
        {
            "username": "user2",
            "user_static_id": "1235rgasd8",
            "userImgLink": usrIcon
        },
        {
            "username": "user3",
            "user_static_id": "1235rgasd6",
            "userImgLink": usrIcon
        },
        {
            "username": "user4",
            "user_static_id": "1235rgasd7",
            "userImgLink": usrIcon
        },
        {
            "username": "user5",
            "user_static_id": "1235rgasd9",
            "userImgLink": usrIcon
        }
    ];

    return {
        type: UPDATE_USERLIST,
        userList: userList
    };
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