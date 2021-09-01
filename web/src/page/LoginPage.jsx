import styled from 'styled-components';
import {Helmet} from "react-helmet";

import { connect } from 'react-redux';
import { userLogin } from '../reducers/ConnectedUserReducer';

import 'bootstrap/dist/css/bootstrap.min.css';
import '../asset/font/font.css';


// imgs
import LogoImg from '../asset/img/logo.svg';
const LoginPage = (props) => {
    
    const hostToStr = "127.0.0.1";
    // 로그인 여부 확인
    if(props.maximumVolume !== undefined && props.maximumVolume != -1) {
        // 로그인 성공
        props.history.push("/storage/root");
    }

    const loginBtnEvent = async (e) => {
        e.preventDefault();

        let email = e.target.email.value;
        let password = e.target.password.value;

        // 빈 문자열 확인
        if(email === "") {
            alert("Please Write your email");
        } else if(password === "") {
            alert("Please Write your password");
        } else {
            // 로그인 시도
            props.userLogin(email, password);
        }
    }

    return (
        <Layer>
            <Helmet>
                <title>MicroCloudChip-NATURAL</title>
            </Helmet>
            <Container>
                <center>
                    <img src={LogoImg} alt="logo" width="60%" style={{ marginBottom: "15px" }}/>
                    <p>server: {hostToStr}</p>
                    <LoginSection onSubmit={loginBtnEvent}>
                        <EditSection>
                            <EditLabel>EMAIL</EditLabel>
                            <EditText type="text" name="email" />
                        </EditSection>
                        <EditSection>
                            <EditLabel>PSWD</EditLabel>
                            <EditText type="password" name="password" />
                        </EditSection>
                        <LoginBtn>LOGIN</LoginBtn>
                    </LoginSection>
                </center>
            </Container>
        </Layer>
    );
}

const mapStateToProps = (state) => {
    return state.ConnectedUserReducer;
};

export default connect(mapStateToProps, {
    userLogin
})(LoginPage);

const Layer = styled.div`
    background-color: #1E1E1E;
    padding-left: 35%;
    padding-right: 35%;
    height: 100vh;
    padding-top: 10%;
    color: #1DB21D;
    font-family: DungGeunMo;
    font-size: 1.6em;
`
const Container = styled.div`
    position: relative;
`
const LoginSection = styled.form`
    padding: 10px;
    margin-top: 40px;
`
const EditSection = styled.div`
    display: flex;
    margin-bottom: 20px;
`
const EditLabel = styled.label`
    width: 20%;
    text-align: left;
`
const EditText = styled.input`
    width: 80%;
    border: 1px solid #1DB21D;
    background-color: #1E1E1E;
    color: #1DB21D;
    border-radius: 8px;
`
const LoginBtn = styled.button`
    width: 100%;
    background-color: #1DB21D;
    color: #1E1E1E;
    border-radius: 5px;
    border: none;
`