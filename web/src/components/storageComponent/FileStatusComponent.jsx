// Icons
import dirImg from '../../asset/img/icons/dir.svg';
import audioFileImg from '../../asset/img/icons/audio-file.svg';
import exeFileImg from '../../asset/img/icons/exe-file.svg';
import imgFileImg from '../../asset/img/icons/img-file.svg';
import pdfFileImg from '../../asset/img/icons/pdf-file.svg';
import txtFileImg from '../../asset/img/icons/txt-file.svg';
import otherFileImg from '../../asset/img/icons/unknown-file.svg';
import videoFileImg from '../../asset/img/icons/video-file.svg';

import multiFileImg from '../../asset/img/icons/multiple-file-icon.svg';
import multiDirImg from '../../asset/img/icons/multiple-dirs-icon.svg';
import multiAllImg from '../../asset/img/icons/multiple-all-icon.svg';

import styled from "styled-components";
import { Image, Button } from "react-bootstrap";

import ExampleImg from '../../asset/img/icons/dir.svg'
import { connect } from "react-redux";

const FileStatusComponent = (props) => {

    let selectedDirList = props.dirList;


    // 컴포넌트에 출력될 데이터들
    let filename = "";
    let imgUrl = "";
    
    
    if(!selectedDirList.length) {
        // 선택된 파일이 없음
        return (
            <Layout>
                <h5>선택된 파일 없음</h5>
            </Layout>
        );
    }

    // 선택된 파일이 한 개 일 경우
    else if(selectedDirList.length == 1) {

        let splited = selectedDirList[0].split('/');
        filename = splited[0];
        let fileType = splited[1];
        
        // TODO: 해당 파일에 대한 정보를
        // 서버로부터 받아와야 함

        if(fileType == "dir") {
            // 디렉토리
            return (
                <Layout>
                    <center style={{ marginBottom: "40px" }}>
                        <Image src={dirImg} width="140px" height="140px" />
                    </center>
                
                    <div style={{ marginBottom: "40px" }}>
                        <TextLayer>
                            <KeyLayer>디렉토리이름</KeyLayer>
                            <ValueLayer>{filename}</ValueLayer>
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
            )
        } else {
            let imgUrl = "";
            switch(fileType) {
                case 'text': imgUrl = txtFileImg; break;
                case 'exe': imgUrl = exeFileImg; break;
                case 'pdf': imgUrl = pdfFileImg; break;
                case 'image': imgUrl = imgFileImg; break;
                case 'audio': imgUrl = audioFileImg;  break;
                case 'video': imgUrl = videoFileImg; break;
                case 'other': imgUrl = otherFileImg; break;
                default: imgUrl = otherFileImg; break;

            }
            return (
                <Layout>
                    <center style={{ marginBottom: "40px" }}>
                        <Image src={imgUrl} width="140px" height="140px" />
                    </center>
                
                    <div style={{ marginBottom: "40px" }}>
                        <TextLayer>
                            <KeyLayer>파일 이름</KeyLayer>
                            <ValueLayer>{filename}</ValueLayer>
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
            )
        }
    } else {
        // 여러개
        let imgUrl = ""
        let fileTypes = selectedDirList.map((data) => data.split('/')[1]);
        let dirCount = fileTypes.filter(t => 'dir' == t).length;
        if(dirCount == 0) {
            // 파일만 선택한 경우
            imgUrl = multiFileImg;
        } else if(dirCount == fileTypes.length) {
            // 폴더만 선택한 경우
            imgUrl = multiDirImg;
        } else {
            // 섞어서 선택한 경우
            imgUrl = multiAllImg;
        }
        return (
            <Layout>
                <center style={{ marginBottom: "40px" }}>
                    <Image src={imgUrl} width="140px" height="140px" />
                </center>
                <div style={{ marginBottom: "40px" }}>
                    <TextLayer>
                        <KeyLayer>선택된 갯수</KeyLayer>
                        <ValueLayer>{fileTypes.length}</ValueLayer>
                    </TextLayer>
                </div>
                <Button variant="success" style={{ width: "100%", marginBottom: "15px"}}>다운로드</Button>
                <Button variant="danger" style={{ width: "100%", marginBottom: "15px"}}>삭제</Button>
            </Layout>
        );
    }
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