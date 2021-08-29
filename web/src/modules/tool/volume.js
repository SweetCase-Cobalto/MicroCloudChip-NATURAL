// KB 기준이다

const VOLUME_TYPES = {
    "BYTE": Math.pow(10, -3),
    "KB": Math.pow(10, 0),
    "MB": Math.pow(10, 3),
    "GB": Math.pow(10, 6),
    "TB": Math.pow(10, 9)
}

export function volume_label_to_raw(_type, _vol) {
    return _vol * VOLUME_TYPES[_type]
}