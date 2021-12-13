// KB 기준이다

const VOLUME_TYPES = {
    "BYTE": Math.pow(10, -3),
    "KB": Math.pow(10, 0),
    "MB": Math.pow(10, 3),
    "GB": Math.pow(10, 6),
    "TB": Math.pow(10, 9)
}

export function volume_label_to_raw(_type, _vol) {
    // Label -> 실제 데이터 용량(KB 기준)
    return _vol * VOLUME_TYPES[_type]
}


// 소수점 버림
export function floorVolume(_val, _zfill) {
    return Math.floor(_val * Math.pow(10, _zfill)) / Math.pow(10, _zfill); 
}
export const convertRawVolumeToString = (value) => {
    // Byte 단위의 Raw 크기값을 string을 변환
    let unit = 'BYTE';

    if(value < Math.pow(10, 3))         { unit = 'KB'; }
    else if(value < Math.pow(10, 6))    { unit = 'MB'; value = (value / Math.pow(10, 3)); }
    else if(value < Math.pow(10, 9))    { unit = 'GB'; value = (value / Math.pow(10, 6)); }
    else                                { unit = 'TB'; value = (value / Math.pow(10, 9)); }

    // 소수점 이하 세자리 버림
    value = Math.floor(value * 1000) / 1000;
    return `${value} ${unit}`;
}