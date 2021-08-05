// 파일 및 디렉토리 선택 여부 데이터

export const UPDATE_DIRS = "SELECTED_DIR_REDUCER/UPDATE_DIRS";

export const updateDirs = (dirListMap) => {
    // 자료형은 Map이어야 한다
    // User와는 다르게 다중 선택이 있기 때문이다.
    // 같은 이름이지만 타입(디렉토리, 파일)이 다르기 때문에
    // key를 이와 같이 정의한다
    //      [filename]/[isDir]
    // value는 선택 여부(true/false)
    return {
        type: UPDATE_DIRS,
        dirListMap
    }
};

const initialState = {
    dirListMap: undefined
}

export const SelectedDirReducer = (state = initialState, action) => {
    switch(action.type) {
        case UPDATE_DIRS:
            return {
                ...state,
                dirListMap: action.dirListMap
            };
        default:
            return state;
    }
};