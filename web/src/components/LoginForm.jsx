import React from 'react';
import styled from 'styled-components';
import { Colors } from '../variables/color';
import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';
import { Form } from 'react-bootstrap';
import { connect } from 'react-redux';
import { updateTokenInReducer, resetTokenReducer } from '../reducers/TokenReducer';
import { loginToServer } from '../connection/user';
import URL from '../asset/config.json';

// Image Import
import LogoImg from '../asset/img/logo.svg';
import { ViewErrorCodes } from '../variables/errors';

const LoginForm = (props) => {
    // 로그인 폼
    
    const loginBtnEvent = async (e) => {

        // 로그인 이벤트
        e.preventDefault();     // 디버깅을 위한 상태유지

        const pswd = e.target.pswd.value;
        const email = e.target.email.value;

        // 로그인
        const result = await loginToServer(URL.URL, email, pswd);

        // 실패여부 확인
        if(result.err == ViewErrorCodes.CLIENT_FAILED) {
            alert("Login Failed");
            props.resetTokenReducer();
        } else if(result.err == ViewErrorCodes.SERVER_FAILED) {
            alert("Failed from server");
            props.resetTokenReducer();
        } else {
            // Success
            props.updateTokenInReducer(result.id, result.token);
            window.location.href = "/storage/root";
        }
    }



    const InputForm = () => {
        // 로그인 입력 폼
        return (
            <InputFormLayout onSubmit={loginBtnEvent}>
                <Form>
                    <Form.Group className="mb-3" style={{ marginTop: "30px" }}>
                        <Form.Control type="email" placeholder="Enter Email" id="email" />
                    </Form.Group>
                    <Form.Group className="mb-3" style={{ marginTop: "20px" }}>
                        <Form.Control type="password" placeholder="Enter Password" id="pswd" />
                    </Form.Group>
                    <button type="submit" className="custombutton-access" style={{ width: "100%", marginTop: "40px" }}>Login</button>
                </Form>
            </InputFormLayout>
        );
    }

    const MobileForm = () => {
        // 모바일 에디션
        const isMobile = useMediaQuery(ResponsiveQuery.MOBILE);
        return (
            (isMobile) &&
            <MobileLayout>
                <center>
                    <img src={LogoImg} alt="logo" style={{ marginBottom: "30px" }}/>
                    <InputForm />
                </center>
            </MobileLayout>
        );
    }
    const PCForm = () => {
        // 데스크탑, 태블릿 에디션
        const isPC = useMediaQuery(ResponsiveQuery.PC);
        const isTablet = useMediaQuery(ResponsiveQuery.TABLET);
        return (
            (isPC || isTablet) &&
            <PCLayout>
                <center>
                    <img src={LogoImg} alt="logo" style={{ marginBottom: "30px" }}/>
                    <InputForm />
                </center>
            </PCLayout>
        )
    }

    // 이미 데이터가 저장되어 있으면 바로 storage로 넘김
    if(props.loginStatus.id != null && props.loginStatus.token)
        window.location.href = "/storage/root";


    // 최종 렌더링
    return (
        <div>
            <MobileForm />
            <PCForm />
        </div>
    );
}
// 리덕스 돌리기용
const mapStateToProps = (state) => (
    {loginStatus: state.TokenReducer }
)
export default connect(mapStateToProps, { updateTokenInReducer, resetTokenReducer })(LoginForm);

// PC 버전 레이아웃
const PCLayout = styled.div`
    padding: 40px 80px 40px 80px;
    marginTop: 300px;
    width: 500px;
    background: #EEEEEE;
    border: 1px solid ${Colors.LOGIN_FORM_LINE};
`;
const MobileLayout = styled.div`
    padding: 20px 40px 20px 40px;
    marginTop: 200px;
    width: 300px;
    background: #EEEEEE;
    border: 1px solid ${Colors.LOGIN_FORM_LINE};
`
// 로그인 폼 레이아웃
const InputFormLayout = styled.div`
`