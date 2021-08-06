// 선택된 유저 표시
// account 페이지에서 유저에 대한 정보를 우측에 나타내기 위해 사용

export const SELECT_USER = "SELECTED_ACCOUNT_REDUCER/SELECT_USER";

export const selectUser = (selectedUserStaticId) => {
    return {
        type: SELECT_USER,
        selectedUserStaticId
    }
};

const initialState = {
    selectedUserStaticId: undefined
}

export const SelectedAccountReducer = (state = initialState, action) => {
    
    switch(action.type) {
        case SELECT_USER:
            return {
                ...state,
                selectedUserStaticId: action.selectedUserStaticId
            };
        default:
            return state;
    }
};