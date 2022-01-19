import { ErrorCodes } from "../variables/errors";

const GET = "DIRECTORYLIST_REDUCER_GET";

export const getDirectoryListReducer = (
    _uri, _fileList, _dirList, _dirIinfo, _errCode
    // backend에서 갖고온 데이터 그대로 사용한다.
) => {
    // errCode가 0이어야 성공
    if(_errCode != ErrorCodes.ERR_SUCCESS) {
        // get Error
        return {
            currentRoot: [],     // 현재 루트
            fileList:   [],     // 파일 리스트
            dirList:    [],     // 디렉토리 리스트
            curInfo:    undefined,  // 현재 디렉토리 정보
            errCode:    _errCode,  // 에러 코드
        }
    } else {
        
        res = {
            // 출력될 데이터
            currentRoot: undefined,
            fileList:   [],     // 파일 리스트
            dirList:    [],     // 디렉토리 리스트
            curInfo:    _dirInfo,  // 현재 디렉토리 정보
            errCode:    _errCode,  // 에러 코드
        }

        // file/dir 데이터 정제
        res.fileList = _fileList.map((f) => {
            return {
                "filename": f.name,
                "type": f.type,
                "isDir": false,
                "isShared": false,  // 공유 여부
            }
        });
        res.dirList = _dirList.map((d) => {
            return {
                "filename": d,
                "type": "dir",
                "isDir": true,
                "isShared": false,
            }
        });

        // 현재 루트 여부
        // 최상위 루트 판정: 루트가 1개만 있으면 최상위 루트
        // 두개 이상이면 하위 디렉토리이므로 뒤로가기를 추가한다
        if(_uri.length > 1)
        {
            res.dirList.unshift({
                "filename": "..",
                "isDir": true,
                "type": "dir",
                "isShared": false,
            })
        }
        return res;
    }
}

const initialState = {
    currentRoot: [],     // 현재 루트
    fileList:   [],     // 파일 리스트
    dirList:    [],     // 디렉토리 리스트
    curInfo:    undefined,  // 현재 디렉토리 정보
    errCode:    undefined,  // 에러 코드
}

export const DirectoryListReducer = {

}