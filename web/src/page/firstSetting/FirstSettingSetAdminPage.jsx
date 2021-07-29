import styled from 'styled-components';

import 'bootstrap/dist/css/bootstrap.min.css';
import '../../asset/font/font.css';

// imgs
import LogoImg from '../../asset/img/logo.svg';

const FirstSettingSetAdminPage = ({ history }) => {

    const hostToStr = "127.0.0.1";

    const btnEvent = (e) => {

        history.push("/firstsetting/setdatabase");
    }

    return (
        <Layer>
            <Container>
                <center>
                    <img src={LogoImg} alt="logo" width="60%" style={{ marginBottom: "20px" }}/>
                    <p>Server: {hostToStr}</p>
                    <h4>사용할 아이디와 패스워드를 입력하세요</h4>
                    <Section onSubmit={btnEvent}>
                        <EditSection>
                            <EditLabel>NAME</EditLabel>
                            <EditText type="text" />
                        </EditSection>

                        <EditSection>
                            <EditLabel>PSWD</EditLabel>
                            <EditText type="password" />
                        </EditSection>

                        
                        <EditSection>
                            <EditLabel>PSWD(RE)</EditLabel>
                            <EditText type="password" />
                        </EditSection>

                        <Btn type="submit">NEXT</Btn>
                    </Section>
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
    font-size: 1.4em;
`
const Section = styled.form`
    padding: 10px;
    margin-top: 40px;
`
const Container = styled.div`
    position: relative;
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
const Btn = styled.button`
    width: 100%;
    background-color: #1DB21D;
    color: #1E1E1E;
    border-radius: 5px;
    border: none;
`
export default FirstSettingSetAdminPage;