import axios from 'axios';
import {useState} from 'react';
import {Helmet} from "react-helmet";

import CONFIG from '../asset/config.json';
import fileDownload from 'js-file-download';

const SharedFilePage = (props) => {

    const READY = "ready";
    const ERROR = "error";
    const OK = "ok"

    let sharedId = props.match.params.sharedId;
    const URL = `${CONFIG.URL}/server/storage/shared/file/${sharedId}`;

    const [isConnected, setConnected] = useState({
        "status": READY,
        "filename": undefined
    });
    
    if(isConnected['status'] == READY) {
        // Server Connection
        axios.get(URL, { params: { "mode": "info" } })
        .then((r) => {
            let data = r.data;
            if(data.code == 0) {
                // success;
                setConnected({
                    "status": OK,
                    "filename": data.data.filename
                })
            } else {
                alert("해당 파일이 만료되었거나 유효하지 않습니다.");
                setConnected({
                    "status": ERROR,
                    "filename": undefined
                })
            }
        }).catch((e) => {
            alert("서버와의 연결에 실패했습니다.");
        });

        return (
            <div>
                <title>Microcloudchip Shared Downloader</title>
                <meta property="og:title" content="Microcloudchip Share Downloader" />
                <div>
                    <p>공유 여부 확인 중</p>
                </div>
            </div>
        )
    } else if(isConnected['status'] == OK) {

        const clickEvent = () => {
            // Server Connection For Download
            axios.get(URL, { 
                crossDomain: true,
                withCredentials: true,
                responseType: 'blob' })
            .then((r) => {
                // Data Checkintg
                let data = r.data;
                console.log(data.type);
                if(data == 'application/json') {
                    // Failed
                    alert("해당 파일의 공유가 만료되었습니다.");
                    setConnected({
                        "status": ERROR,
                        "filename": undefined
                    })
                } else {
                    // Downloading
                    fileDownload(data, isConnected['filename']);
                }
                
            }).catch((e) => {
                console.log(e);
                alert("서버와의 연결이 끊어졌습니다.");
            });
        }

        return (
            <div>
                <Helmet>
                    <title>Microcloudchip Shared Downloader</title>
                    <meta property="og:image" content="" />
                    <meta property="og:title" content="Microcloudchip Share Downloader" />
                    <meta property="og:description" content="You Can download shared file!"/>
                </Helmet>
                <center>
                    <p>파일명: {isConnected['filename']}</p>
                    <p>다운로드 할 수 있습니다.</p>
                    <button onClick={clickEvent}>다운로드</button>
                </center>
            </div>
        )
    } else {
        return (
            <div>
                <Helmet>
                    <title>Microcloudchip Shared Downloader</title>
                    <meta property="og:title" content="Microcloudchip Share Downloader" />
                    <meta property="og:description" content="Download is Expired"/>
                </Helmet>
                <center>
                    <p>해당 파일의 공유기간이 만료되었습니다.</p>
                </center>
            </div>
        )
    }

}

export default SharedFilePage;