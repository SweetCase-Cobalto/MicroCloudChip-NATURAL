import axios from "axios";

export async function cookieRequestedImgUrlToAvailableUrl(url, token) {
    // 주로 이미지나 기타 파일들을 웹상에서 바로 보여줄 때 사용
    // URL를 요청해서 Raw 데이터를 얻은 다음 FrontEnd상의 URL로 전환

    let blob = await axios.get(url, {
        headers: { "Set-Cookie": token },
        withCredentials: true,
        crossDomain: true,
        responseType: 'blob'
    }).then((res) => res.data);
    

    return window.URL.createObjectURL(blob);
}