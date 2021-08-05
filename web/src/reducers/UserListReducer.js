/* 얘는 Admin만 접근해야 한다  */
import usrIcon from '../asset/img/icons/user-icon.svg';

export const UPDATE_USERLIST = "USER_LIST_REDUCER/UPDATE_USER_LIST";

export const updateUserList = () => {
    // TODO Connect to Server
    // admin을 제외한 나머지 데이터 불러오기
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