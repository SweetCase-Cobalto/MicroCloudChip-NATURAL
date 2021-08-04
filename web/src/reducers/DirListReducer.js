export const UPDATE_DIRLIST = "DIRLISTREDUCER/UPDATE_DIRLIST";

export const updateDirList = (newUrl) => {

    // TODO Get DirList From server
    // 서버 API를 연결할 경우
    // asnyc로 전환하고 axios 함수 앞에 await 추가

    let newFileList = [
        {
            "filename": "file1.txt",
            "modify-date": "2021-01-01 4:13am",
            "isDir": false,
            "file-type": "text",
            "size-str": "1KB"
        },
        {
            "filename": "mymusic.mp3",
            "modify-date": "2021-01-01 4:13am",
            "file-type": "audio",
            "size-str": "3MB",
            "isDir": false,
        }
    ]
    let newDirList = [
        {
            "filename": "mydir",
            "modify-date": "2021-01-01 4:13am",
            "file-type": "none",
            "size-str": "11",
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