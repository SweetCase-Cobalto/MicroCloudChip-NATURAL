import axios from 'axios';
import CONFIG from '../../asset/config.json';

import {volume_label_to_raw} from '../tool/volume';

export async function getUserInformationFromServer(staticID, token) {
    // 유저 정보 갱신
    const URL = CONFIG.URL + "/server/user/" + staticID;

    
    try {
        // 쿠키에 토큰 쳐넣고 돌리기
        let data = await axios.get(URL, {
            headers: {
                "Set-Cookie": token
            },
            crossDomain: true,
            withCredentials: true,
        });
        data = data.data;
        if(data.code != 0) {
            return data;
        } else {

            // Volume_type calcuate
            let capacity_volume = volume_label_to_raw(
                data['user-info']['volume-type']['type'],
                data['user-info']['volume-type']['value']
            )
            let used_volume = volume_label_to_raw(
                data['used-volume']['type'],
                data['used-volume']['value']
            )

            return {
                "code": data.code,
                "data": {
                    "userName": data['user-info'].name,
                    "email": data['user-info'].email,
                    'isAdmin': data['user-info']['is-admin'],
                    "maximumVolume": capacity_volume,
                    "usedVolume": used_volume,
                    "token": token,
                }
            };
        }
    } catch (err) {
        return err;
    }
}