// 파일 및 디렉토리 선택 여부 데이터

export const UPDATE_DIRS = "SELECTED_DIR_REDUCER/UPDATE_DIRS";

export const updateDirs = (dirList) => {
    // 자료형은 Array이어야 한다
    // redux는 불변성을 지향하기 때문에 Map은 안먹힌다.
    // value:     [filename]/[fileType]
    return {
        type: UPDATE_DIRS,
        dirList
    }
};

const initialState = {
    dirList: []
}

export const SelectedDirReducer = (state = initialState, action) => {
    switch(action.type) {
        case UPDATE_DIRS:
            return {
                ...state,
                dirList: action.dirList
            };
        default:
            return state;
    }
};