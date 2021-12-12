import axios from 'axios';
import { BackendUris } from '../variables/backendUris';
import { ErrorCodes, ViewErrorCodes } from '../variables/errors';

export const loginToServer = async (serverUrl, email, pswd) => {
    // 로그인에 성공할 경우 토큰과 고유 아이디 출력

    const uri = `${serverUrl}${BackendUris.LOGIN}`;
    const formData = new FormData();

    formData.append("email", email);
    formData.append("pswd", pswd);

    return await axios.post(uri, formData, { withCredentials: true }).then((res) => {
        let data = res.data;
        if(data.code == ErrorCodes.ERR_SUCCESS) {
            // Success
            return { "err": ViewErrorCodes.SUCCESS, "id": data.data['static-id'], "token": data.data['token']};
        } else {
            // Failed
            return { "err": ViewErrorCodes.CLIENT_FAILED };
        }
    }).catch(() => {
        // 서버상의 에러
        return { "err": ViewErrorCodes.SERVER_FAILED };
    })   
}

export const logoutToServer = async (serverUri, token) => {
    const uri = `${serverUri}${BackendUris.LOGOUT}`;
    
    return await axios.get(uri, {
        headers: {"Set-Cookie": token},
        withCredentials: true,
        crossDomain: true,
    }).then((res) => {
        let data = res.data;
        if(data.code == ErrorCodes.ERR_SUCCESS) {
            // Success
            return {"err": ViewErrorCodes.SUCCESS };
        } else {
            return {"err": ViewErrorCodes.CLIENT_FAILED};
        }
    }).catch(() => {
        return {"err": ViewErrorCodes.SERVER_FAILED};
    })
}