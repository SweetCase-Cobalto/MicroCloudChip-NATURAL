import styled from "styled-components";
import {Image, Form, Button} from "react-bootstrap";
import { connect } from "react-redux";
import { updateMyInfo } from "../../reducers/ConnectedUserReducer";
import { useHistory } from "react-router-dom";
import { useState } from "react";

import BootstrapDropdownSelector from "../atomComponents/BootstrapDropdownSelector";
import axios from "axios";

import { ErrorCodes } from '../../modules/err/errorVariables';

import CONFIG from '../../asset/config.json';

const AccountUpdaterForm = (props) => {

    const [targetUserInfo, setTargetUserInfo] = useState(undefined);

    /*
        계정을 수정하거나
        생성 할 때 사용하는 폼

        TODO: 버튼 이벤트 함수 구현 필요
    */
    const history = useHistory();

    let isNameChangeDisabled = false;             // admin의 아이디와 이메일 계정은 수정할 수 없다.
    let isEmailChangeDisabled = false;            // 수정할 때 email은 수정할 수 없다.


    let actionType = props.actionType;  // 수정 or 생성
    let target = props.target;          // my: 자신, other: 다른 사람
    let btnTitle = "수정"               // 생성일 경우 제출 버튼 타이틀은 생성으로 바뀐다.
    let isVolumeTypeDisabled = true;    // volume Type은 변경할 수 없으므로 변경 폼일 경우 disable 처리한다.
    let targetStaticId = props.targetStaticId;  // 해당 사용자의 정보변경할 때 사용되는 고정 아이디
    let curImgLink = props.usrImgLink; // User Icon
    let changedIconImage = undefined; // 변경될 이미지 (변경하지 않을 경우 undefinedf로 처리한다.)

    // Volume Type Data
    let volumeSelectItems = ["TEST 1KB[테스트용]", "GUEST 5GB", "USER 20GB", "HEAVIER 100GB"];
    let selectedVolumeItem = volumeSelectItems[0]

    // volume Type Changed Event
    const volumeTypeChangedEvent = (selectedItem) => {
        selectedVolumeItem = selectedItem;
    }

    // 데이터를 수정할 때 사용되는 Default Value
    let nameDefaultValue = undefined;
    let emailDefaultValue = undefined;

    // Select Type
    if(actionType == "modify") {
        // 계정 정보를 수정하는 경우
        isEmailChangeDisabled = true;
        if(target == "my") {
            // 자기 자신을 수정하는 경우
            nameDefaultValue = props.userName;
            emailDefaultValue = props.email;
            targetStaticId = props.id;

            if(props.isAdmin) {
                isNameChangeDisabled = true;
            }
        } else {
            /*
                Admin이 해당 사용자의 정보 수정을 원하는 경우이다.
                사용자 staticId를 활용하여 서버로부터 전체적인
                유저 데이터를 갖고 온다.
            */
            // 아래는 예시 데이터
            
            const URL = `${CONFIG.URL}/server/user/${targetStaticId}`;
            
            if(targetUserInfo == undefined) {
                // 아직 서버로부터 데이터를 받지 못한 경우
                
                axios.get(URL, {
                    headers: {"Set-Cookie": props.token},
                    withCredentials: true,
                    crossDomain: true
                }).then((response) => {
                    let data = response.data;
                    if(data.code == 0) {
                        // 전송 성공
                        let info = data['user-info'];

                        let userInfo = {
                            name: info['name'],
                            email: info['email']
                        }
                        setTargetUserInfo(userInfo);
                    } else {
                        alert("권한이 없습니다.");
                        window.location.href = "/";
                    }
                }).catch((err) => {
                    alert("서버와의 통신에서 문제가 발생했습니다.");
                    window.location.href = "/accounts";
                })
                

                // Loading
                return <div>Loading</div>
            }

            // 서버로부터 데이터를 받은 경우
            nameDefaultValue = targetUserInfo.name;
            emailDefaultValue = targetUserInfo.email;
        }
    } else {
        btnTitle = "추가"
        isVolumeTypeDisabled = false;
    }

    const applyClickEvent = (e) => {
        e.preventDefault();
        
        // 데이터 갖고오기
        let userName = e.target.id.value;
        let pswd = e.target.pswd.value;
        let pswdRepeat = e.target.pswdRepeat.value;
        let email = e.target.email.value;
        let volumeType = selectedVolumeItem.split(' ')[0]

        let userNameRegex = /^[a-zA-Z0-9]{4,16}$/;
        
        // Null값 확인하기
        if(userName == "" || pswd == "" || pswdRepeat == "" || email == "") {
            alert("입력란을 채워주세요");
            return;
        }
        if(!userNameRegex.test(userName)) {
            alert("잘못된 유저 이름 입니다.");
            return;
        }
        if(pswd.length < 8 || pswd.length > 128) {
            alert("패스워드는 8자 이상 128자 이하 입니다.");
            return;
        }
        if(pswd != pswdRepeat) {
            alert("패스워드가 일치하지 않습니다.");
            return;
        }

        
        // 유저 추가 / 수정 에 따라 요청이 달라진다
        if(actionType == 'add') {

            // Admin 이름을 사용해선 안된다.
            if(userName == 'admin') {
                alert('admin이 이름인 계정을 생성할 수 없습니다.');
                return;
            }

            // 유저 추가
            const formData = new FormData();
            formData.append('name', userName);
            formData.append('email', email);
            formData.append('password', pswd);
            formData.append('volume-type', volumeType);

            // 전송
            let URL = `${CONFIG.URL}/server/user`;
            axios.post(URL, formData , {
                headers: {'Set-Cookie': props.token},
                withCredentials: true,
                crossDomain: true
            }).then((response) => {
                let data = response.data;
                if(data.code == 0) {
                    alert("계정 생성 성공");
                } else {
                    // Error Code 별로 다른 문구 출력
                    if(data.code = ErrorCodes.ERR_AUTH_ACCESS_ERR) {
                        alert("이메일은 중복될 수 없습니다.");
                    } else {
                        alert("계정 생성 실패");
                    }
                }
                window.location.href = "/accounts";
            }).catch((err) => {
                alert("전송 오류");
                window.location.href = "/acocunts";
            })
        } else if(actionType == 'modify') {
            // 수정
            
            // 수정 요청을 위한 FormData 생성
            const formData = new FormData();
            formData.append('name', userName);
            formData.append('password', pswd);

            
            if(changedIconImage == undefined)
                // 변경 할 파일을 정하지 않은 경우
                formData.append('img-changeable', 0);
            else {
                // 정한 경우
                formData.append('img-changeable', 1);
                formData.append('img', changedIconImage);
            }

            // URL 세팅
            const URL = `${CONFIG.URL}/server/user/${targetStaticId}`;
            axios.patch(URL, formData, {
                headers: {'Set-Cookie': props.token},
                withCredentials: true,
                crossDomain: true
            }).then((response) => {
                let data = response.data;

                if(data.code == 0) {
                    // 변경 성공
                    alert("변경에 성공했습니다.");
                } else {
                    alert("변경에 실패했습니다.");
                    alert(data.code);
                }
            }).catch((err) => {
                alert("전송 오류");
            }).finally(() => {
                // 페이지 나가기
                if(props.isAdmin) {
                    // 관리자 계정
                    window.location.href = "/accounts";
                } else {
                    // 일반 계정
                    window.location.href = "/settings";
                }
            })
            
        }
    }
    return (
        <EditLayer>
            <form>
                <Image src={curImgLink}
                    width="170px" 
                    height="170px" 
                    style={{ backgroundColor: "gray", cursor: "pointer" }}
                    id="renderedSelectedImg"
                    onClick={ () => {document.getElementById("newImgUrl").click()}}
                    roundedCircle />
                <input type="file" name="newImgUrl" 
                    id="newImgUrl" accept=".jpg, .png" 
                    onChange={e => {
                        // 이미지가 바뀔 경우 이미지 갱신
                        let selectedFile = e.target.files[0]
                        let imgReader = new FileReader();
                        imgReader.onload = () => {
                            // 이미지 변경
                            document.getElementById("renderedSelectedImg").src = imgReader.result;
                        }
                        imgReader.readAsDataURL(selectedFile);
                        // 파일에 업로드 하기 위한 파일 데이터 생성
                        changedIconImage = selectedFile;

                    }} hidden/>

            </form>
            <EditForm onSubmit={applyClickEvent}>
                <Form.Group style={{ marginBottom: "20px" }} >
                    <Form.Label>아이디</Form.Label>
                    <Form.Control type="text" 
                                    name="id" 
                                    placeholder="4자 이상 18자 이하 영어 및 숫자만" 
                                    disabled={isNameChangeDisabled} 
                                    defaultValue={actionType == "add" ? "" : nameDefaultValue} />
                </Form.Group>

                <div style={{ display: "flex", marginBottom: "20px" }}>
                
                    <Form.Group style={{ marginRight: "5%", width: "50%" }} >
                        <Form.Label>비밀번호</Form.Label>
                        <Form.Control type="password" name="pswd" placeholder="8자 이상 128자 이하" />
                    </Form.Group>

                    <Form.Group style={{  width: "50%" }} >
                        <Form.Label>비밀번호 재입력</Form.Label>
                        <Form.Control type="password" name="pswdRepeat" placeholder="다시 한번 더" />
                    </Form.Group>
                </div>

                <Form.Group style={{ marginBottom: "30px" }} >
                    <Form.Label>이메일</Form.Label>
                    <Form.Control type="email" 
                                    name="email" 
                                    placeholder="example@example.com"
                                    disabled={isEmailChangeDisabled}
                                    defaultValue={actionType == "add" ? "" : emailDefaultValue} />
                </Form.Group>

                <Form.Group style={{ marginBottom: "30px", display: isVolumeTypeDisabled ? "none" : "block" }}>
                    <Form.Label>용량 타입</Form.Label>
                    <BootstrapDropdownSelector 
                        itemList={volumeSelectItems} 
                        onChangedEvent={volumeTypeChangedEvent}
                    />
                </Form.Group>
            
                <div style={{ display: "flex", float: "right" }} >
                    <Button variant="success" type="submit"
                            style={{ width: "100px", marginRight: "20px", backgroundColor: "#137813"}} 
                            >{btnTitle}</Button>
                    <Button variant="secondary" 
                            style={{ width: "100px", backgroundColor: "#4C4D4C" }}
                            onClick={() => history.goBack()}>취소</Button>
                </div>
            </EditForm>
        </EditLayer>
    );
}

const mapStateToProps = (state) => {
    return state.ConnectedUserReducer;
}
export default connect(mapStateToProps, {
    updateMyInfo
})(AccountUpdaterForm);


const EditLayer = styled.div`
    margin-top: 40px;
    display: flex;
`
const EditForm = styled.form`
    padding-left: 40px;
    width: 100%;
`