import styled from 'styled-components';
import {useState} from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import '../../asset/font/font.css';

// imgs
import LogoImg from '../../asset/img/logo.svg';

const FirstSettingSetDatabasePage = ({ history }) => {

    const hostToStr = "127.0.0.1";
    const [dbSelected, setDbSelected] = useState('');



    // MySQLComponent
    const MysqlSection = () => {

        const [isBtnDisabled, setIsBtnDisabled] = useState(false);
        const [isConnectPassed, setIsConnectPassed] = useState(false);
        // 이건 프로토타입 테스트용임
        const mySQLConnectTestEvent = (e) => {
            e.preventDefault();
            
            setIsBtnDisabled(true);

            // 성공시
            setIsBtnDisabled(false);
            setIsConnectPassed(true);

        }

        return (
            <div>
                <Section>
                    <div style={{ fontSize: '0.7em', border: "1px solid #1DB21D", padding: "10px"}}>
                        <p>외부 데이터베이스 서버(MySQL)로부터 연결을 테스트합니다.</p>
                        <p>외부 데이터베이스를 사용하면 스토리지를 제외한 다른 데이터의 복구 지원을 받으실 수 있습니다.(정식 버전부터만 가능)</p>
                    </div>
                    <EditSection style={{ marginTop: "40px" }} >
                        <EditLabel>HOST</EditLabel>
                        <EditText type="text" />
                    </EditSection>

                    <EditSection style={{ marginTop: "20px" }} >
                        <EditLabel>PORT</EditLabel>
                        <EditText type="number" />
                    </EditSection>

                    <EditSection style={{ marginTop: "20px" }} >
                        <EditLabel>USER</EditLabel>
                        <EditText type="text" />
                    </EditSection>
                
                    <EditSection style={{ marginTop: "20px" }} >
                        <EditLabel>PSWD</EditLabel>
                        <EditText type="password" />
                    </EditSection>


                    <EditSection style={{ marginTop: "20px" }} >
                        <EditLabel>DB</EditLabel>
                        <EditText type="text" />
                    </EditSection>

                    <Btn onClick={mySQLConnectTestEvent} disabled={isBtnDisabled}>TestConnect</Btn>
                </Section>
                <Btn disabled={!isConnectPassed}>Start</Btn>
            </div>
        );
    }

    // SQLITE Component
    const SqliteSection = () => {
        return (
            <Section>
                <div style={{ fontSize: '0.7em', border: "1px solid #1DB21D", padding: "10px", marginBottom: "30px"}}>
                    <p>내부에 데이터베이스를 생성합니다. </p>
                    <p>가장 간단하게 서버를 관리할 수 있으나, 사후 복구지원을 받으실 수 없습니다.</p>
                </div>
                <Btn>시작하기</Btn>
            </Section>
        );
    }

    const DatabaseSelectSection = () => {
        if(dbSelected == 'sqlite') {
            return <SqliteSection />
        } else if(dbSelected == 'mysql') {
            return <MysqlSection />
        } else {
            return <Section />
        }
    }
    return (
        <Layer>
            <Container>
                <center>
                    <img src={LogoImg} alt="logo" width="60%" style={{ marginBottom: "20px" }}/>
                    <p>Server: {hostToStr}</p>
                    <h4>사용할 데이터베이스를 선택하세요</h4>
                    <div onChange={e => {
                        setDbSelected(e.target.value);
                    }}>
                        <label style={{ marginRight: "30px" }}>
                            <RadioBtn type="radio" name="db_info" value="mysql" 
                                        style={{ color: "white" }}/>외부 DB(MYSQL)
                        </label>
                        <label style={{ marginRight: "30px" }}>
                            <RadioBtn type="radio" name="db_info" value="sqlite" 
                                style={{ color: "white" }} />내부 DB(SQLITE)
                        </label>
                    </div>
                    <DatabaseSelectSection />
                </center>
            </Container>
        </Layer>
    );
}
const Layer = styled.div`
    background-color: #1E1E1E;
    padding-left: 35%;
    padding-right: 35%;
    height: 120vh;
    padding-top: 10%;
    color: #1DB21D;
    font-family: DungGeunMo;
    font-size: 1.4em;
`
const RadioBtn = styled.input`
    margin-right: 10px;
`

const Section = styled.form`
    padding: 10px;
    margin-top: 10px;
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
export default FirstSettingSetDatabasePage;