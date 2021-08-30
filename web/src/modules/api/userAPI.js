import axios from 'axios';
import CONFIG from '../../asset/config.json';

import {volume_label_to_raw} from '../tool/volume';


export async function getUserInformationFromServer(staticID) {
    // 유저 정보 갱신
    const URL = CONFIG.URL + "/server/user/" + staticID
    try {
        let data = await axios.get(URL, { withCredentials: true});
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
                    "id": id,
                    "userName": data['user-info'].name,
                    "email": data['user-info'].email,
                    'isAdmin': data['user-info']['is-admin'],
                    "maximumVolume": capacity_volume,
                    "usedVolume": used_volume
                }
            };
        }
    } catch (err) {
        return err;
    }
}