import styled from "styled-components";
import { Image, ProgressBar } from "react-bootstrap";
import { useState } from "react";

import { syncUserInfo, setUserInfoEmpty } from "../../reducers/ConnectedUserReducer";

import { connect } from "react-redux";

import {getUserInformationFromServer} from '../../modules/api/userAPI';

const MyAccountStatusComponent = (props) => {

    const [ isConnectedWithServer, setIsConnectedwithServer] = useState(false)

    console.log(props);

    // 서버 연결 프로세스
    async function connectToServer() {
        if(!isConnectedWithServer) {
            let result = await getUserInformationFromServer(props.id);
            
            // Code 측정
            if(result.code == 0) {
                // 유저 정보가 맞는 경우
                let info = result.data;
                props.syncUserInfo(info);
                setIsConnectedwithServer(true);

            } else {
                // 로그인 페이지로 이동
                props.setUserInfoEmpty();
                setIsConnectedwithServer(true);
                window.location.assign("/");
            }
        }
    }
    connectToServer()

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
    let usrIcon = props.usrImgLink;                 // 업로드한 유저 이미지

    let gage = (usedStorage / capacityStorage) * 100; // 사용용량 Percentage

    if(!isConnectedWithServer) {
        // 로딩 페이지 구현 필요
        return <div>Loading</div>
    } else {

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
                        <span style={{color: "#137813" }}>{usedStorage}G</span>
                        <span>/{capacityStorage}G</span>
                    </div>
                    <ProgressBar style={{ width: "100%", backgroundColor: "#7D7D7D"}} striped variant="success" now={gage} />
                </div>
            </Layout>
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