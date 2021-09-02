import CONFIG from '../asset/config.json';
import axios from 'axios';

export const UPDATE_DIRLIST = "DIR_LIST_REDUCER/UPDATE_DIR_LIST";

export const updateDirList = (newUrl, token, static_id) => {
    // 현재 위치의 디렉토리와 파일을 갖고온다.

    // 검색 URL
    const URL = CONFIG.URL + "/server/storage/data/dir/" + static_id + "/" + newUrl;

    return dispatch => {
        // 서버 통신
        axios.get(URL, {
            headers: { "Set-Cookie": token },
            withCredentials: true,
            crossDomain: true
        })
        .then((response) => {
            // 통신 성공
            let data = response.data;
            if(data.code == 0) {
                // 정상적으로 데이터가 들어온 경우
                
                // 서버로부터 받은 Raw 데이터 수집
                let raw_file_list = data.data.list.file;
                let raw_dir_list = data.data.list.dir;
                
                // 프론트 단에 출력하기 위한 데이터로 정제
                const __newFileList = raw_file_list.map((f) => {
                    return {
                        "filename": f.name,
                        "type": f.type,
                        "isDir": false
                    }
                })
                const __newDirList = raw_dir_list.map((d) => {
                    return {
                        "filename": d['dir-name'],
                        "type": "dir",
                        "isDir": true
                    }
                });

                // 최상위 루트인지 확인
                // 최상위 루트인 경우 뒤로가기 추가 X

                if(newUrl.length > 1) {
                    // 즉 newUrl에 루트가 2개 이상이면 최상위 루트가 아니다
                    // 따라서 뒤로가가 (..를 누른다.)
                    __newDirList.push({
                        "filename": "..",
                        "isDir": true,
                        "file-type": "dir",
                    })
                }

                return dispatch ({
                    type: UPDATE_DIRLIST,
                    curUrl: newUrl,
                    newFileList: __newFileList,
                    newDirList: __newDirList,
                    curInfo: data.data.info
                })
            } else {
                return dispatch ({
                    type: UPDATE_DIRLIST,
                    curUrl: newUrl,
                    newFileList: [],
                    newDirList: [],
                    curInfo: data.code
                })
            }
        })
    }
};

const initialState = {
    curUrl : [],
    fileList : [],
    directoryList : [],
    curInfo: undefined
};

export const DirListReducer = (state = initialState, action) => {
    switch(action.type) {
        case UPDATE_DIRLIST:
            return {
                curInfo: action.curInfo,
                curUrl: action.newUrl,
                fileList: action.newFileList,
                directoryList: action.newDirList
            };
        default:
            return state;
    }
};