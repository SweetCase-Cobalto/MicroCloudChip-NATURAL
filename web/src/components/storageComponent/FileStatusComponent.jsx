import styled from "styled-components";
import { Image, Button } from "react-bootstrap";

import ExampleImg from '../../asset/img/icons/dir.svg'
import { connect } from "react-redux";

const FileStatusComponent = (props) => {

    // FIXME: props 갱신 안됨
    let dirMap = props.dirListMap;

    console.log(props);
    let selectedFileType = []
    let selectCounter = 0

    if(dirMap !== undefined) {

        // Calculate
        let keys = Array.from(dirMap.keys());
        keys.map((key) => {
            let isSelected = dirMap.get(key);
            if(isSelected) {
                // 선택한 경우
                selectCounter++;
            }
        });
    }

    return (
        <Layout>
            <center style={{ marginBottom: "40px" }}>
                <Image src={ExampleImg} width="140px" height="140px" />
            </center>
            
            <div style={{ marginBottom: "40px" }}>
                <TextLayer>
                    <KeyLayer>파일 이름</KeyLayer>
                    <ValueLayer>file.txt</ValueLayer>
                </TextLayer>

                <TextLayer>
                    <KeyLayer>수정 날짜</KeyLayer>
                    <ValueLayer>2021-01-01 4:13 am</ValueLayer>
                </TextLayer>

                <TextLayer>
                    <KeyLayer>파일 유형</KeyLayer>
                    <ValueLayer>Text</ValueLayer>
                </TextLayer>
                
                <TextLayer>
                    <KeyLayer>용량</KeyLayer>
                    <ValueLayer>1KB</ValueLayer>
                </TextLayer>
            </div>

            <Button variant="success" style={{ width: "100%", marginBottom: "15px"}}>다운로드</Button>
            <div style={{ marginBottom: "15px", display: "flex" }}>
                <Button variant="outline-success" style={{ width: "50%", marginRight: "10%"}}>이름 변경</Button>
                <Button variant="outline-success" style={{ width: "50%"}}>공유 설정</Button>
            </div>
            <Button variant="danger" style={{ width: "100%", marginBottom: "15px"}}>삭제</Button>
        </Layout>
    );
}

const mapStateToProps = (state) => {
    return state.SelectedDirReducer;
}
export default connect(mapStateToProps)(FileStatusComponent);

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