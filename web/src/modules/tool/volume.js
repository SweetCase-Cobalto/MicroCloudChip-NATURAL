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