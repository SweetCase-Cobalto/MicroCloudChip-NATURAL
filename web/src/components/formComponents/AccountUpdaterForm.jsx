import styled from "styled-components";
import {Image, Form, Button} from "react-bootstrap";
import { connect } from "react-redux";
import { updateMyInfo } from "../../reducers/ConnectedUserReducer";
import { useHistory } from "react-router-dom";

import BootstrapDropdownSelector from "../atomComponents/BootstrapDropdownSelector";
import axios from "axios";

import CONFIG from '../../asset/config.json';

const AccountUpdaterForm = (props) => {

    /*
        계정을 수정하거나
        생성 할 때 사용하는 폼

        TODO: 버튼 이벤트 함수 구현 필요
    */
    const history = useHistory();

    let isDisabled = false;             // admin의 아이디와 이메일 계정은 수정할 수 없다.
    let actionType = props.actionType;  // 수정 or 생성
    let target = props.target;          // my: 자신, other: 다른 사람
    let btnTitle = "수정"               // 생성일 경우 제출 버튼 타이틀은 생성으로 바뀐다.
    let isVolumeTypeDisabled = true;    // volume Type은 변경할 수 없으므로 변경 폼일 경우 disable 처리한다.
    let targetStaticId = props.targetStaticId;  // 해당 사용자의 정보변경할 때 사용되는 고정 아이디

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
        if(target == "my") {
            // 자기 자신을 수정하는 경우
            // 일반 사용자는 자기 자신을 수정할 수 없다.
            nameDefaultValue = props.userName;
            emailDefaultValue = props.email;

            if(props.isAdmin) {
                isDisabled = true;
            }
        } else {
            /*
                Admin이 해당 사용자의 정보 수정을 원하는 경우이다.
                TODO: 사용자 staticId를 활용하여 서버로부터 전체적인
                유저 데이터를 갖고 온다.
            */
            // 아래는 예시 데이터
            nameDefaultValue = "exampleName";
            emailDefaultValue = "exampleEmail";
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
            alert("네임은 오직 알파벳 및 숫자로만 작성할 수 있습니다.");
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
                    alert("계정 생성 실패");
                }
                history.push('/accounts');
            }).catch((err) => {
                console.log(err);
                alert("전송 오류");
            })

        }
    }

    return (
        <EditLayer>
            <Image src="holder.js/171x180" width="170px" height="170px" style={{ backgroundColor: "gray" }} roundedCircle />

            <EditForm onSubmit={applyClickEvent}>
                <Form.Group style={{ marginBottom: "20px" }} >
                    <Form.Label>아이디</Form.Label>
                    <Form.Control type="text" 
                                    name="id" 
                                    placeholder="4자 이상 18자 이하 영어 및 숫자만" 
                                    disabled={isDisabled} 
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
                                    disabled={isDisabled} 
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