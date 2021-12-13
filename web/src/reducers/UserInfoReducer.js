const UPDATE = "USERINFO_REDUCER_UPDATE"
const RESET = "USERINFO_REDUCER_RESET"

// 유저 정보 (영구 저장)
const initialState = {
    id: null, token: null, name: null,
    email: null, isAdmin: false,
    volumeType: null,
    capacityVolume: -1,
    usedVolume: -1
}

export const updateUserInfoReducer = (
    // 유저 갱신
    _id, _token, _email, _isAdmin, _name,
    _volumeType, _capacityVolume, _usedVolume
) => (
    {
        "type": UPDATE,
        "data": {
            id: _id, token: _token, name: _name, email: _email,
            isAdmin: _isAdmin, volumeType: _volumeType,
            capacityVolume: _capacityVolume, usedVolume: _usedVolume
        }
    }
)
export const resetUserInfoReducer = () => ({
    "type": RESET
});
// 리셋

export const UserInfoReducer = (state = initialState, action) => {
    switch(action.type) {
        case UPDATE:
            return action.data;
        case RESET:
            return initialState;
        default:
            return initialState;
    }
}