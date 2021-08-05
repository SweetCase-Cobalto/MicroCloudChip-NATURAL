export const UPDATE_DIRLIST = "DIR_LIST_REDUCER/UPDATE_DIR_LIST";

export const updateDirList = (newUrl) => {

    // TODO Get DirList From server
    // 서버 API를 연결할 경우
    // asnyc로 전환하고 axios 함수 앞에 await 추가

    let newFileList = [
        {
            "filename": "file1.txt",
            "isDir": false,
            "file-type": "text"
        },
        {
            "filename": "mymusic.mp3",
            "file-type": "audio",
            "isDir": false,
        }
    ]
    let newDirList = [
        {
            "filename": "mydir",
            "file-type": "none",
            "isDir": true,
        }
    ]

    return {
        type: UPDATE_DIRLIST,
        newUrl: newUrl,
        newFileList: newFileList,
        newDirList: newDirList
    }
};

const initialState = {
    curUrl : [],
    fileList : [],
    directoryList : []
};

export const DirListReducer = (state = initialState, action) => {
    switch(action.type) {
        case UPDATE_DIRLIST:
            return {
                curUrl: action.newUrl,
                fileList: action.newFileList,
                directoryList: action.newDirList
            };
        default:
            return state;
    }
};