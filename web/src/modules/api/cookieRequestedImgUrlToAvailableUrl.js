import axios from "axios";

export async function cookieRequestedImgUrlToAvailableUrl(url, token) {
    let blob = await axios.get(url, {
        headers: { "Set-Cookie": token },
        withCredentials: true,
        crossDomain: true,
        responseType: 'blob'
    }).then((res) => res.data);
    

    return window.URL.createObjectURL(blob);
}