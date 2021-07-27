import styled from 'styled-components';
import {Helmet} from "react-helmet";

import 'bootstrap/dist/css/bootstrap.min.css';
import '../asset/font/font.css';

// imgs
import LogoImg from '../asset/img/logo.svg';

const LoginPage = ({ history }) => {
    
    const hostToStr = "127.0.0.1";

    // Checking if is First Setting
    // TODO Redux 저장 권유
    let isFirst = true;
    if(isFirst) {
        // 처음 세팅으로 이동
        history.push("/firstsetting/setadmin");
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
                    <LoginSection>
                        <EditSection>
                            <EditLabel>NAME</EditLabel>
                            <EditText type="text" />
                        </EditSection>
                        <EditSection>
                            <EditLabel>PSWD</EditLabel>
                            <EditText type="text" />
                        </EditSection>
                        <LoginBtn>LOGIN</LoginBtn>
                    </LoginSection>
                </center>
            </Container>
        </Layer>
    );
}
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
export default LoginPage;