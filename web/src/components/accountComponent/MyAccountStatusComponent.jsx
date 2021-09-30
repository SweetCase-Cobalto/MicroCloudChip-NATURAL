import styled from "styled-components";
import { Image, ProgressBar } from "react-bootstrap";

import { syncUserInfo, setUserInfoEmpty } from "../../reducers/ConnectedUserReducer";
import { connect } from "react-redux";

import { useState } from "react";
import defaultUserIcon from '../../asset/img/icons/user-icon.svg';

import { cookieRequestedImgUrlToAvailableUrl } from  '../../modules/tool/cookieRequestedImgUrlToAvailableUrl';
import { volume_label_to_raw } from "../../modules/tool/volume";


const MyAccountStatusComponent = (props) => {
    // 업로드한 유저 이미지

    const [isConnected, setIsConnected] = useState(0);
    const [usrIcon, setUsrIcon] = useState(undefined);

    if(!isConnected) {
        // 아직 서버와 동기화를 하지 못했다면
        // 동기화 한다.
        props.syncUserInfo(props.id, props.token);
        setIsConnected(isConnected+1);

        return <div>
            Loading
        </div>
    }
    if(props.maximumVolume === undefined || props.maximumVolume == -1 || props.id == "") {
        // 데이터받기에 실패할 경우(대부분 로그인 만료임)
        window.location.href = "/";
    }

    // 이미지 다운로드
    if(isConnected == 1 && usrIcon == undefined) {
        if(props.usrImgLink == defaultUserIcon) {
            // 이미지 없으면 기존 이미지 대체
            setUsrIcon(defaultUserIcon);
        } else {
            // 외부에서 받아와야 한다
            cookieRequestedImgUrlToAvailableUrl(props.usrImgLink, props.token)
            .then((resultUrl) => {
                setUsrIcon(resultUrl);
            })
        }
    }
    
    const convertRawVolumeToString = (value) => {
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

    /*
        내 계정에 대한 정보를 표시하는 컴포넌트
        이름과 이메일, 계급(클라이언트, 어드민)
        그리고 사용 용량이 표기되어야 한다.
        좌측에 표시된다.
    */

    let name = props.userName;
    let email = props.email;
    let type = props.isAdmin ? "admin" : "client";
    let capacityStorage = props.maximumVolume;
    let usedStorage = props.usedVolume;             // 사용하고 있는 용량
    

    // 아이콘 URL이 내부 기본 이미지가 아닐 경우 서버에서 추가로 IMG 데이터를 받아오고
    // URL로 변경해야 한다
    
    if(isConnected == 1 && usrIcon != undefined) {
        let gage = (usedStorage / capacityStorage) * 100; // 사용용량 Percentage
        return (
           <Layout>
               <center style={{ marginBottom: "80px" }} >
                   <Image src={usrIcon} width="150px" height="150px" roundedCircle />
                   <h3 style={{ marginTop: "20px", fontWeight: "bold", color: "#137813" }}>{name}</h3>
                   <p style={{ color: "#707070"}}>{email}</p>
                   <p>{type}</p>
               </center>
               <div style={{ fontWeight: "bold" }}>
                   <div style={{ marginBottom: "15px" }}>
                       <span style={{color: "#137813" }}>{convertRawVolumeToString(usedStorage)}</span>
                       <span>/{convertRawVolumeToString(capacityStorage)}</span>
                   </div>
                   <ProgressBar style={{ width: "100%", backgroundColor: "#7D7D7D"}} striped variant="success" now={gage} />
               </div>
           </Layout>
       );
    } else {
        return (
            <div>Loading</div>
        );
    }

}

const mapStateToProps = (state) => {
    return state.ConnectedUserReducer;
}
export default connect(mapStateToProps, 
    {syncUserInfo, setUserInfoEmpty})(MyAccountStatusComponent);

const Layout = styled.div`
    line-height: 0.4em;

    font-family: "Gothic A1";
    width: 330px;
    margin-right: 20px;

    box-shadow: 2px 2px 3px gray;

    padding-top: 50px;
    padding-bottom: 100px;
    padding-left: 20px;
    padding-right: 20px;
    
    background-color: #EFEFEF;
`