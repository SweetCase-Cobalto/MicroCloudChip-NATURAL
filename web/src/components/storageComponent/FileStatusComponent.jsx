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

import CONFIG from '../../asset/config.json';
import { ErrorCodes } from '../../modules/err/errorVariables';

import styled from "styled-components";
import { Image, Button, Form, Modal, ProgressBar } from "react-bootstrap";

import { floorVolume } from '../../modules/tool/volume';

import fileDownload from 'js-file-download';


import { connect } from "react-redux";
import { useState } from 'react';
import axios from 'axios';

const FileStatusComponent = (props) => {
    /*
        Storage Page의 우측 하단에 배치되어 있는 컴포넌트로
        파일 및 디렉토리의 정보를 나타내는 데 사용한다
    */

    let selectedDirList = props.selectedDir.dirList;    // 선택된 파일 및 디렉토리 리스트
    const [dataInfo, setDataInfo] = useState(undefined);
    // 선택된 데이터에 대한 정보
    /*
        선택된 객체가 한개일 때만 서버로부터 정보 데이터를 가져온다
        선택하지 않거나 다중 선택할 경우 undefined로 전환
    */

    let filename = "";
    // 하나를 선택할 경우 객체 이름이 저장된다.


    // 모달 컴포넌트
    // 파일/디렉토리 삭제/수정할 때 뜨는 모달 Flag
    const [isModifyObjectModalOpen, setIsModifyObjectModalOpen] = useState(false);
    const [isDeleteObjectModalOpen, setIsDeleteObjectModalOpen] = useState(false);
    const [isDeleteMultipleModalOpen, setIsDeleteMultipleModalOpen] = useState(false);
    
    if(!selectedDirList.length) {
        // 선택된 파일이 없음
        // 선택된 파일이 없는데도 dataInfo에 데이터가 남아있다면
        // 없앤다.
        if(dataInfo != undefined)
            setDataInfo(undefined);
        return (
            <Layout>
                <h5>선택된 파일 없음</h5>
            </Layout>
        );
    }

    // 선택된 파일이 한 개 일 경우
    else if(selectedDirList.length == 1) {

        // Reducer에 저장된 선택된 객체의 정보를 갖고온다
        // RAW: 파일이름/파일타입
        // splited => [파일 이름, 파일 타입]
        let splited = selectedDirList[0].split('/');
        filename = splited[0];
        let fileType = splited[1];
        
        if(dataInfo === undefined) {
            // 아직 받아오지 못했거나 다른 파일 및 디렉토리를 선택한 경우
            

            // 서버와 통신하기 위한 URL 생성
            let TARGET_URL = CONFIG.URL + "/server/storage/data/";
            if(fileType == 'dir')
                TARGET_URL += "dir/"
            else
                TARGET_URL += "file/"
            TARGET_URL += props.userInfo.id + "/" + props.parentDir.curUrl.join('/') + "/" + filename;

            // 전송
            axios.get(TARGET_URL, {
                headers: {"Set-Cookie": props.userInfo.token },
                withCredentials: true,
                crossDomain: true
            })
            .then((response) => {
                let data = response.data;
                if(data.code != 0) {
                    // TODO: 오류에 따른 처리 필요
                    alert("오류 발생");
                } else {
                    // 정상적을 데이터를 받는 경우

                    // TODO: data.data.info 데이터가
                    // 받지 못하는 경우에 대한 예외처리가 필요
                    if(fileType == "dir")
                        setDataInfo(data.data.info);
                    else
                        setDataInfo(data.data);
                }
            })
            
            // TODO: 로딩 페이지 구현 필요
            return (<div>
                Loading
            </div>)
        }
        // 정보를 다운받았을 경우
        // 위 서버 통신은 패싱하고 컴포넌트를 리턴한다.

        
        // Events
        const downloadSingleObjectEvent = async () => {

            // 파일 한개 다운로드
            let URL = `${CONFIG.URL}/server/storage/download/single`;

            if(fileType == 'dir') {
               URL += `/dir/`; 
            } else {
                URL += `/file/`;
            }
            URL += `${props.userInfo.id}/${props.parentDir.curUrl.join("/")}/${filename}`;
            
            // 요청
            axios.get(URL, {
                headers: {'Set-Cookie': props.userInfo.token},
                crossDomain: true,
                withCredentials: true,
                responseType: 'blob',
            }).then((response) => {
                let data = response.data;
                if(fileType == 'dir') {
                    fileDownload(data, `${filename}.zip`)
                } else {
                    fileDownload(data, filename);
                }
            }).catch((err) => {
                alert("서버로부터 문제가 발생했습니다.");
                window.location.reload();
            })
            
        }

        
        // Modal Components
        const ModifyObjectModal = () => {
            // 객체 이름 수정 컴포넌트

            const closeEvent = () => setIsModifyObjectModalOpen(false);
            const modifyHandler = (e) => {
                // 이름 변경 요청

                let newName = e.target.newName.value;
                let formData = new FormData();
                
                // URL 과 FormData 세팅
                let URL = CONFIG.URL + "/server/storage/data";
                if(fileType == "dir") {
                    URL += "/dir/";
                    formData.append("dir-name", newName);
                }
                else {
                    URL += "/file/";
                    formData.append("filename", newName);
                }
                URL += props.userInfo.id + "/" + props.parentDir.curUrl.join("/") + "/" +filename;

                // 송신
                
                axios.patch(URL, formData, {
                    headers: {"Set-Cookie": props.userInfo.token },
                    crossDomain: true,
                    withCredentials: true
                }).then((response) => {
                    // 전송 결과 받기
                    let data = response.data;
                    if(data.code == 0) {
                        alert("이름을 변경했습니다.");
                    } else {
                        // 적용 실패
                        if(data.code == ErrorCodes.ERR_DIR_ALEADY_EXISTS_ERR) {
                            // 새로 변경할 이름의 디렉토리가 이미 존재하는 경우
                            alert("해당 이름의 디렉토리가 이미 존재합니다.");
                        } else if(data.code == ErrorCodes.ERR_FILE_ALEADY_EXISTS_ERR) {
                            // 새로 변경 할 이름의 파일ㄹ이 이미 존재하는 경우
                            alert("해당 이름의 파일이 이미 존재합니다.");
                        } else if(data.code == ErrorCodes.ERR_SYSTEM_ABNORMAL_ACCESS_ERR) {
                            // 동일한 이름으로 변경하려는 경우
                            alert("동일한 이름으로 변경할 수 없습니다.");
                        }
                    }
                })
                
            }
            
            let modalTitle = "";
            let keyword = "";
            let placeholder = "";

            // 파일/디렉토리에 따른 문구 세팅
            if(fileType == 'dir') {
               modalTitle = "디렉토리 이름 수정";
               keyword = "디렉토리";
               placeholder = "디렉토리 이름 입력";
            } else {
                modalTitle = "파일 이름 수정"
                keyword = "파일";
                placeholder = "파일 이름 입력 (확장자는 변경되지 않습니다.)";
            }

            const EditComponent = () => {

                /* 파일 이름 수정 컴포넌트
                    따로 분리한 이유는 다음과 같다.
                        - 확장자가 달린 파일일 경우 
                            확장자는 변경되지 않으므로 확장자를 에디터 오른쪼겡
                            보기 쉽게 출력되어야 한다.
                */

                if(fileType == 'dir') {
                    return (
                        <Form.Control type="text" placeholder={placeholder} name="newName"/>
                    )
                } else {
                    let __extension = "";
                    
                    let __splitedFilename = filename.split('.');
                    if(__splitedFilename.length > 1) {
                        // 확장자가 존재하는 경우
                        __extension = __splitedFilename[__splitedFilename.length - 1];
                    }

                    return (
                        <div style={{ display: "flex" }}>
                            <Form.Control type="text" placeholder={placeholder} style={{ marginRight: "10px" }} name="newName" />
                            <h5>.{__extension}</h5>
                        </div>
                    )
                }
            }

            return (
                <Modal
                    show={isModifyObjectModalOpen}
                    onHide={closeEvent}
                    centered
                >
                    <Modal.Header closeButton>
                        <Modal.Title>{modalTitle}</Modal.Title>
                    </Modal.Header>
                    <Form onSubmit={modifyHandler}>
                        <Modal.Body>
                            <Form.Group className="mb-3" controlId="newDirectoryName">
                                <Form.Label>새로운 {keyword} 이름을 입력하세요</Form.Label>
                                <EditComponent />
                            </Form.Group>
                        </Modal.Body>
                        <Modal.Footer>
                            <Button variant="success" type="submit">수정</Button>
                            <Button variant="secondary" onClick={closeEvent}>취소</Button>
                        </Modal.Footer>
                    </Form>
                </Modal>
            )
        }

        const DeleteObjectModal = () => {
            
            const closeEvent = () => { setIsDeleteObjectModalOpen(false); }
            const deleteEvent = () => {
                
                // URL 세팅
                let URL = CONFIG.URL + "/server/storage/data/";
                if(fileType == 'dir') {
                    URL += "dir/";
                } else {
                    URL += "file/";
                }
                URL += `${props.userInfo.id}/${props.parentDir.curUrl.join('/')}/${filename}`;

                // 삭제
                axios.delete(URL, {
                    headers: {'Set-Cookie': props.userInfo.token },
                    crossDomain: true,
                    withCredentials: true
                }).then((response) => {
                    let data = response.data;
                    if(data.code == 0) {
                        alert("삭제에 성공했습니다.");
                    } else {
                        alert("삭제에 실패했습니다.");
                    }
                    window.location.reload();
                })
            }

            return (
                <Modal
                    show={isDeleteObjectModalOpen}
                    onHide={closeEvent}
                    centered
                >
                    <Modal.Header closeButton>
                        <Modal.Title>파일 및 디렉토리 삭제</Modal.Title>
                    </Modal.Header>
                    
                    <Modal.Body>
                            <h5>정말로 삭제하시겠습니까?</h5>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="danger" onClick={deleteEvent}>삭제</Button>
                        <Button variant="secondary" onClick={closeEvent}>취소</Button>
                    </Modal.Footer>

                </Modal>
            )
        }

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
                            <ValueLayer>{dataInfo['create-date']}</ValueLayer>
                        </TextLayer>
                    
                        <TextLayer>
                            <KeyLayer>파일 갯수</KeyLayer>
                            <ValueLayer>{dataInfo['file-size']}</ValueLayer>
                        </TextLayer>
                    </div>
    
                    <Button variant="success" style={{ width: "100%", marginBottom: "15px"}} onClick={() =>{downloadSingleObjectEvent()}}>다운로드</Button>
                    <div style={{ marginBottom: "15px", display: "flex" }}>
                        <Button variant="outline-success" style={{ width: "100%"}} onClick={() => setIsModifyObjectModalOpen(true)}>이름 변경</Button>
                    </div>
                    <Button variant="danger" style={{ width: "100%", marginBottom: "15px"}} onClick={() => setIsDeleteObjectModalOpen(true)}>삭제</Button>

                    <ModifyObjectModal />
                    <DeleteObjectModal />
                </Layout>
            )
        } else {
            // 파일
            let imgUrl = "";
            fileType = fileType.toLowerCase();
            switch(fileType) {
                // 파일 타입에 따른 파일 이미지 세팅
                case 'text': imgUrl = txtFileImg; break;
                case 'exe': imgUrl = exeFileImg; break;
                case 'pdf': imgUrl = pdfFileImg; break;
                case 'image': imgUrl = imgFileImg; break;
                case 'audio': imgUrl = audioFileImg;  break;
                case 'video': imgUrl = videoFileImg; break;
                case 'other': imgUrl = otherFileImg; break;
                default: imgUrl = otherFileImg; break;

            }
            let __printedVolume = `${floorVolume(dataInfo['size']['size-volume'], 3)} ${dataInfo['size']['size-type']}`
            
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
                            <KeyLayer>생성 날짜</KeyLayer>
                            <ValueLayer>{dataInfo['create-date']}</ValueLayer>
                        </TextLayer>
    
                        <TextLayer>
                            <KeyLayer>파일 유형</KeyLayer>
                            <ValueLayer>{fileType}</ValueLayer>
                        </TextLayer>
                    
                        <TextLayer>
                            <KeyLayer>용량</KeyLayer>
                            <ValueLayer>{__printedVolume}</ValueLayer>
                        </TextLayer>
                    </div>
    
                    <Button variant="success" style={{ width: "100%", marginBottom: "15px"}} onClick={() =>{downloadSingleObjectEvent()}}>다운로드</Button>
                    <div style={{ marginBottom: "15px", display: "flex" }}>
                        <Button variant="outline-success" style={{ width: "100%"}} onClick={() => setIsModifyObjectModalOpen(true)}>이름 변경</Button>
                    </div>
                    <Button variant="danger" style={{ width: "100%", marginBottom: "15px"}} onClick={() => setIsDeleteObjectModalOpen(true)}>삭제</Button>

                    <ModifyObjectModal />
                    <DeleteObjectModal />
                </Layout>
            )
        }
    } else {
        // 여러개
        
        // 여러개기 때문에 전에 선택된 단일 파일 및 디렉토리 정보는 갖다버려 ㅋ
        if(dataInfo != undefined)
            setDataInfo(undefined);

        let imgUrl = ""

        // 파일 리스트 (파일 타입 / 파일 이름)
        let fileTypes = [];
        let fileNames = [];

        selectedDirList.map((data) => {
            // 할당
            let splited = data.split('/');

            fileNames.push(splited[0]);
            fileTypes.push(splited[1]);
        })
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

        // 다중 파일/디렉토리 삭제 Modal
        const MultipleDeleteObjectModal = () => {

            // 컴포넌트 변화를 위한 useState
            const [deleteProcess, setDeleteProcess] = useState({
                "targetFileName": undefined,
                "deletedFileNum": -1,
                /*
                    targetFileName: 삭제 중인 파일 이름
                    deletedFileNum: 삭제한 파일 갯수
                        -1 => 작업 전
                        0 ~ => 삭제한 파일 수
                        == fileNames.length => 파일 삭제 완료
                */
            })

            
            // 제거 대상 파일/디렉토리 리스트 컴포넌트
            let DeletedObjectListShowComponentList = [];

            for(let i = 0; i < fileNames.length; i++) {
                // 파일 순회 돌면서 파일 리스트 컴포넌트 만들기

                let __fileTypeForPrint = "";
                let __fontColor = "";

                // File 타입: Dir -> 디렉토리, Other -> 파일
                if(fileTypes[i] == 'dir') {
                    __fileTypeForPrint = "[Directory]";
                    __fontColor = "blue"
                } else {
                    __fileTypeForPrint = "[File]";
                    __fontColor = "black";
                }
                
                // 컴포넌트 만들기
                DeletedObjectListShowComponentList.push(
                    <p style={{ fontSize: "0.9em", marginBottom: "-2px"}} key={i}>
                        <strong style={{ color: `${__fontColor}` }}>{__fileTypeForPrint}</strong>:{fileNames[i]}
                    </p>
                )
            }
            
            const closeEvent = () => { setIsDeleteMultipleModalOpen(false); }
            // 창닫기 이벤트

            const deleteEvent = async () => {
                // 삭제 이벤트
                
                // URL 세팅
                let URL = CONFIG.URL + "/server/storage/data"

                // 진행 중 표시
                setDeleteProcess({
                    "targetFileName": fileNames[0],
                    "deletedFileNum": 0,
                })

                for(let i = 0; i < fileNames.length; i++) {
                    // 순회 돌면서 파일 및 디렉토리 없애버리기

                    let TARGET_URL = URL;
                    if(fileTypes[i] == 'dir') {
                        TARGET_URL += "/dir";
                    } else {
                        TARGET_URL += "/file";
                    }
                    
                    TARGET_URL += `/${props.userInfo.id}/${props.parentDir.curUrl.join('/')}/${fileNames[i]}`;

                    // Delete
                    // 파일, 디렉토리에 따라 다른 URL을 송신한다.
                    let result = await axios.delete(TARGET_URL, {
                        headers: {'Set-Cookie': props.userInfo.token},
                        withCredentials: true,
                        crossDomain: true,
                    }).then((response) => response.data)
                    .catch((err) => {
                        // 서버 연결 시도 실패
                        return {
                            "code": ErrorCodes.ERR_AXIOS_FAILED,
                            "data": err,
                        };
                    });

                    // 전송 결과
                    if(result.code == ErrorCodes.ERR_AXIOS_FAILED) {
                        // Axios Error: 주로 서버와 연결이 끊어졌을 대 발생한다.
                        alert("서버로부터 연결이 끊어졌습니다.");
                        break;
                    } else if(result.code == 0) {
                        // 삭제 성공
                        let nextFileName = undefined;
                        
                        // 다음 삭제 대상 파일 출력
                        if(i == fileNames.length - 1) {
                            nextFileName = "삭제 완료";
                        } else {
                            nextFileName = fileNames[i + 1];
                        }
                        console.log(nextFileName);
                        setDeleteProcess({
                            "targetFileName": nextFileName,
                            "deletedFileNum": i + 1,
                        });

                    } else {
                        // 서버상의 에러
                        alert("파일에 삭제에 문제가 생겼습니다.");
                        break;
                    }

                
                }
            }

            // 하위 컴포넌트
            const ModalBodyComponent = () => {
                // Modal.Body 컴포넌트
                if(deleteProcess.deletedFileNum == -1 && deleteProcess.targetFileName === undefined) {
                    // 작업 전
                    return (
                        <Modal.Body>
                            <h5>다음과 같은 파일 및 디렉토리를 삭제합니다.</h5>
                            <div style={{
                                margin: "10px", padding: "10px",
                                height: "300px",  width: "100%",
                                overflow: "scroll",
                                border: "1px solid gray",
                            }}>
                                {DeletedObjectListShowComponentList}
                            </div>
                            <h5>삭제하시겠습니까?</h5>         
                        </Modal.Body>
                    )
                } else if(0 <= deleteProcess.deletedFileNum && deleteProcess.deletedFileNum < fileNames.length ) {
                    // 진행 중
                    let percentage = (deleteProcess.deletedFileNum / fileNames.length) * 100;
                    return (
                        <Modal.Body>
                            <h5>Delete: {fileNames[deleteProcess.deletedFileNum]}</h5>
                            <ProgressBar striped variant="success" now={percentage} />
                        </Modal.Body>
                    )
                } else {
                    // 완료
                    return (
                        <Modal.Body>
                            <h5>삭제 완료</h5>
                            <ProgressBar striped variant="success" now={100} />
                        </Modal.Body>
                    );
                }
            }
            const ModalFooterComponent = () => {
                // Modal.Footer 컴포넌트
                if(deleteProcess.deletedFileNum == -1 && deleteProcess.targetFileName === undefined) {
                    // 작업 전
                    return (
                        <Modal.Footer>
                            <Button variant="danger" onClick={deleteEvent}>삭제</Button>
                            <Button variant="secondary" onClick={closeEvent}>취소</Button>
                        </Modal.Footer>
                    )
                } else if (0 <= deleteProcess.deletedFileNum && deleteProcess.deletedFileNum < fileNames.length ) {
                    // 작업중
                    return (
                        <Modal.Footer />
                    )
                } else {
                    // 작업 완료
                    return (
                        <Modal.Footer>
                            
                            <Button variant="success" onClick={() => {
                                window.location.reload();
                            }}>확인</Button>
                        </Modal.Footer>
                    )
                }
            }
            return (
                <Modal
                    show={isDeleteMultipleModalOpen}
                    onHide={closeEvent}
                    centered
                >
                    <Modal.Header>
                        <Modal.Title>파일 및 디렉토리 삭제</Modal.Title>
                    </Modal.Header>
                    <ModalBodyComponent />
                    <ModalFooterComponent />
                </Modal>
            )
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
                <Button variant="danger" style={{ width: "100%", marginBottom: "15px"}} onClick={() => {setIsDeleteMultipleModalOpen(true)}}>삭제</Button>

                <MultipleDeleteObjectModal />
            </Layout>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        "selectedDir": state.SelectedDirReducer,
        "userInfo": state.ConnectedUserReducer,
        "parentDir": state.DirListReducer
    }
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