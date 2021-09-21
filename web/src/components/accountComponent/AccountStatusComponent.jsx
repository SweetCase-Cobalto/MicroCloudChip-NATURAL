import styled from "styled-components";
import { Image, Button } from "react-bootstrap";

import ExampleImg from '../../asset/img/icons/user-icon.svg';
import defaultUserIconImg from '../../asset/img/icons/user-icon.svg';
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { useState } from "react";

import axios from 'axios';
import CONFIG from '../../asset/config.json';
import { cookieRequestedImgUrlToAvailableUrl } from '../../modules/tool/cookieRequestedImgUrlToAvailableUrl';

const AccountStatusComponent = (props) => {
    /*
        Account 페이지에서
        해당 계정을 클릭하면 우측 화면에 나오는
        Acocunt 상태를 표시하는 컴포넌트
        수정 및 삭제 버튼 기능도 포함
    */
    const [userInfo, setUserInfo] = useState(undefined);

    if(props.selected.selectedUserStaticId === undefined) {
        return (
            // 사용자 선택 안함
            <Layout>
                <center style={{ marginBottom: "40px" }}>
                    <Image src={ExampleImg} width="140px" height="140px" roundedCircle />
                    <h5 style={{ marginTop: "40px", fontWeight: "bold" }}>수정 및 삭제할 사용자를 선택하세요</h5>
                </center>
            </Layout>
        );
    } else {
        let modifyUrl = "/accounts/modify/"+props.selected.selectedUserStaticId;

        if(userInfo == undefined || userInfo.staticId != props.selected.selectedUserStaticId) {
            // 직전에 유저를 선택 안했거나 다른 유저를 선택한 경우
            // 사로운 선택된 유저 정보로 갱신한다.
            
            // 사용자 데이터 불러오기
            let REQ_URL = CONFIG.URL + '/server/user/' + props.selected.selectedUserStaticId;

            axios.get(REQ_URL, {
                headers: { 'Set-Cookie': props.userInfo.token },
                withCredentials: true,
                crossDomain: true
            }).then((response) => {
                let data = response.data;
                if(data.code == 0) {
                    // 데이터 받기 성공
                    let req = {
                        name: data['user-info']['name'],
                        email: data['user-info']['email'],
                        staticId: data['user-info']['static-id'],
                        volumeType: `${data['user-info']['volume-type']['value']} 
                            ${data['user-info']['volume-type']['type']}`
                    }
                    
                    // 아이콘 이미지 여부
                    req['iconUrl'] = ('user-icon' in data['user-info'] ? 
                        `${CONFIG.URL}${data['user-info']['user-icon']}` : defaultUserIconImg )

                    setUserInfo(req);
                } else {
                    alert("권한 없음");
                    window.location.href = "/";
                }
            })

            return <div>
                Loading
            </div>
        }

        const removeUserEvent = (e) => {


            let willRemove = confirm("정말로 삭제하시겠습니까?");
            
            if(willRemove) {
                // 진짜 삭제
                const URL = `${CONFIG.URL}/server/user/${props.selected.selectedUserStaticId}`;

                // 전송
                axios.delete(URL, {
                    headers: {'Set-Cookie': props.userInfo.token},
                    withCredentials: true,
                    crossDomain: true
                }).then((response) => {
                    let data = response.data;

                    if(data.code == 0) {
                        alert("삭제 성공");
                    } else {
                        alert("삭제에 실패했습니다. 이미 삭제된 것일 수도 있습니다.");
                    }

                }).catch((err) => {
                    alert("서버와의 통신에 문제가 생겼습니다.");
                }).finally(() => {
                    window.location.reload();
                })
            }
        }

        const UserImgComponent = () => {
            // 유저 이미지 컴포넌트
            const [iconImgUrl, setIconImgUrl] = useState(undefined);

            if(iconImgUrl == undefined) {
                // 이미지 파일이 업는 경우 기존 이미지로 대체
                if(userInfo.iconUrl == defaultUserIconImg) {
                    setIconImgUrl(defaultUserIconImg);
                } else {
                    console.log(userInfo.iconUrl);
                    cookieRequestedImgUrlToAvailableUrl(userInfo.iconUrl, props.userInfo.token)
                        .then((resultUrl) => { setIconImgUrl(resultUrl); });
                }
                return <Image style={{backgroundColor: "gray"}} width="140px" height="140px" roundedCircle />
            } else {
                return <Image src={iconImgUrl} width="140px" height="140px" roundedCircle />
            }
        }

        return (
            <Layout>
                <center style={{ marginBottom: "40px" }}>
                    <UserImgComponent />
                </center>
                
                <div style={{ marginBottom: "40px" }}>
                    <TextLayer>
                        <KeyLayer>아이디</KeyLayer>
                        <ValueLayer>{userInfo.name}</ValueLayer>
                    </TextLayer>
    
                    <TextLayer>
                        <KeyLayer>이메일</KeyLayer>
                        <ValueLayer>{userInfo.email}</ValueLayer>
                    </TextLayer>
    
                    <TextLayer>
                        <KeyLayer>사용가능용량</KeyLayer>
                        <ValueLayer>{userInfo.volumeType}</ValueLayer>
                    </TextLayer>
                </div>

                <Link to={modifyUrl}>
                    <Button variant="success" 
                            style={{ width: "100%", marginBottom: "15px"}}>수정</Button>
                </Link>
                <Button variant="danger" style={{ width: "100%", marginBottom: "15px"}} onClick={removeUserEvent}>삭제</Button>
            </Layout>
        );
    }
}
const mapStateProps = (state) => {
    return {
        "selected": state.SelectedAccountReducer,
        "userInfo": state.ConnectedUserReducer
    }
}
export default connect(mapStateProps)(AccountStatusComponent);

const Layout = styled.div`
    line-height: 0.4em;

    font-family: "Gothic A1";
    width: 330px;
    margin-left: 20px;

    box-shadow: 2px 2px 3px gray;

    padding-top: 50px;
    padding-bottom: 100px;
    padding-left: 20px;
    padding-right: 20px;

    background-color: #EFEFEF;
`
const TextLayer = styled.div`
    width: 100%;
    display: flex;
    margin-bottom: 10px;
`
const KeyLayer = styled.p`
    width: 40%;
    color: #3A3A3A;
`
const ValueLayer = styled.p`
    width: 60%;
    font-weight: bold;
`