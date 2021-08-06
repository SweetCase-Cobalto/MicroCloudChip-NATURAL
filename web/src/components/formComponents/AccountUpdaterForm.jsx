import styled from "styled-components";
import {Image, Form, Button} from "react-bootstrap";
import { connect } from "react-redux";
import { updateMyInfo } from "../../reducers/ConnectedUserReducer";
import { useHistory } from "react-router-dom";

import BootstrapDropdownSelector from "../atomComponents/BootstrapDropdownSelector";

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
    let volumeSelectItems = ["5G", "20G", "100G", "500G"];
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
        if(target == "my") {

            nameDefaultValue = props.userName;
            emailDefaultValue = props.email;

            if(props.isAdmin) {
                isDisabled = true;
            }
        } else {
            // 해당 정보 데이터를 갖고오기
            nameDefaultValue = "exampleName";
            emailDefaultValue = "exampleEmail";
        }
    } else {
        btnTitle = "추가"
        isVolumeTypeDisabled = false;
    }

    return (
        <EditLayer>
            <Image src="holder.js/171x180" width="170px" height="170px" style={{ backgroundColor: "gray" }} roundedCircle />

            <EditForm>
                <Form.Group style={{ marginBottom: "20px" }} >
                    <Form.Label>아이디</Form.Label>
                    <Form.Control type="text" 
                                    name="id" 
                                    placeholder="6자 이상 12자 이하 영어만" 
                                    disabled={isDisabled} 
                                    defaultValue={actionType == "add" ? "" : nameDefaultValue} />
                </Form.Group>

                <div style={{ display: "flex", marginBottom: "20px" }}>
                
                    <Form.Group style={{ marginRight: "5%", width: "50%" }} >
                        <Form.Label>비밀번호</Form.Label>
                        <Form.Control type="password" name="pswd" placeholder="8자 이상 24자 이하" />
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
                    <Button variant="success" 
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