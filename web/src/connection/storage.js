import axios from 'axios';
import { BackendUris } from '../variables/backendUris';
import { ErrorCodes, ViewErrorCodes } from '../variables/errors';


export const getDirectoryInformation = async (_serverUri, _user, _curRoot, _token) => {
    // 디렉토리 정보 가져오기

    const rootStr = _curRoot.join('/');
    const uri = `${_serverUri}${BackendUris.DIRINFO}/${_user}/${rootStr}`;

    return await axios.get(uri, {
        headers: {"Set-Cookie": _token},
        withCredentials: true,
        crossDomain: true,
    }).then((res) => { 
        let data = res.data;
        return {
            "viewErrCode": ViewErrorCodes.SUCCESS,
            data: data,
        }
    })
    .catch(() => {
        return {
            "viewErrCode": ViewErrorCodes.SERVER_FAILED,
            data: undefined
        }
    })
}