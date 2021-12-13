import axios from 'axios';
import { BackendUris } from '../variables/backendUris';
import { ErrorCodes, ViewErrorCodes } from '../variables/errors';
import { volume_label_to_raw } from '../variables/volume';

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

/* 토큰만 제거하기 때문에 당장은 사용하지 않는다
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
*/

export const getUserInformation = async(serverUri, token, staticId) => {
    // 유저 데이터 갖고오기
    const uri = `${serverUri}${BackendUris.USER_URI}/${staticId}`

    return await axios.get(uri, {
        headers: {"Set-Cookie": token},
        withCredentials: true,
        crossDomain: true,
    }).then((res) => {
        let data = res.data;

        if(data.code != ErrorCodes.ERR_SUCCESS) {
            // Failed
            if(data.code == ErrorCodes.ERR_LOGIN_CONNECTION_EXPIRE_ERR)
                // 만료 에러
                return {"err": ViewErrorCodes.CLIENT_FAILED, "msg": "Login session expired"};
            else
                // 그 외의 에러
                return {"err": ViewErrorCodes.CLIENT_FAILED, "msg": "Unknown Error"};
        } else {
            // Success

            // 가용 및 사용 용량을 KB 단위로 환산
            let capacityVolume = volume_label_to_raw(
                data['user-info']['volume-type']['type'],
                data['user-info']['volume-type']['value']
            )
            let usedVolume = volume_label_to_raw(
                data['used-volume']['type'],
                data['used-volume']['value']
            )
            return {
                "err": ViewErrorCodes.SUCCESS,
                "data": {
                    userName: data['user-info'].name,
                    email: data['user-info'].email,
                    isAdmin: data['user-info']['is-admin'],
                    maximumVolume: capacityVolume,
                    usedVolume: usedVolume,
                    staticId: data['user-info']['static-id'],
                    newToken: data['new-token'],
                    volumeType: data['user-info']['volume-type'],
                }
            }
        }
    }).catch(() => {
        return {"err": ViewErrorCodes.SERVER_FAILED, "msg": "Server Error"};
    })
}