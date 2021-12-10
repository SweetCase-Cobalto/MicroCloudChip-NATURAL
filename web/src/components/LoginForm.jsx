import styled from 'styled-components';
import { Colors } from '../variables/color';
import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';
import { Form, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

// Image Import
import LogoImg from '../asset/img/logo.svg';

// import custom Module
import '../asset/css/customButton.css';

const loginBtnEvent = (e) => {
    // 로그인 이벤트
    e.preventDefault();
    alert(e.target.pswd.value);
}

const LoginForm = () => {
    // 로그인 폼

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
                    <Button type="submit" className="custombutton-access" style={{ width: "100%", marginTop: "40px" }}>Login</Button>
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

    // 최종 렌더링
    return (
        <div>
            <MobileForm />
            <PCForm />
        </div>
    );
}
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
export default LoginForm;