import styled from "styled-components";
import { Image, Button } from "react-bootstrap";

import ExampleImg from '../../asset/img/icons/user-icon.svg';
import { connect } from "react-redux";
import { Link } from "react-router-dom";

const AccountStatusComponent = (props) => {
    /*
        Account 페이지에서
        해당 계정을 클릭하면 우측 화면에 나오는
        Acocunt 상태를 표시하는 컴포넌트
        수정 및 삭제 버튼 기능도 포함
    */

    if(props.selectedUserStaticId === undefined) {
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
        // 사용자 선택
        // TODO: 여기서 서버로부터 유저 정보를 불러와야 한다.
        // TODO: 수정 및 삭제 버튼에 대한 이벤트 구현 필요

        let modifyUrl = "/accounts/modify/"+props.selectedUserStaticId;
        return (
            <Layout>
                <center style={{ marginBottom: "40px" }}>
                    <Image src={ExampleImg} width="140px" height="140px" roundedCircle />
                </center>
                
                <div style={{ marginBottom: "40px" }}>
                    <TextLayer>
                        <KeyLayer>아이디</KeyLayer>
                        <ValueLayer>{props.selectedUserStaticId}</ValueLayer>
                    </TextLayer>
    
                    <TextLayer>
                        <KeyLayer>이메일</KeyLayer>
                        <ValueLayer>seokbong60@gmail.com</ValueLayer>
                    </TextLayer>
    
                    <TextLayer>
                        <KeyLayer>용량 제한</KeyLayer>
                        <ValueLayer>100G</ValueLayer>
                    </TextLayer>
                </div>

                <Link to={modifyUrl}>
                    <Button variant="success" 
                            style={{ width: "100%", marginBottom: "15px"}}>수정</Button>
                    <Button variant="danger" style={{ width: "100%", marginBottom: "15px"}}>삭제</Button>
                </Link>
            </Layout>
        );
    }
}
const mapStateProps = (state) => {
    return state.SelectedAccountReducer;
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