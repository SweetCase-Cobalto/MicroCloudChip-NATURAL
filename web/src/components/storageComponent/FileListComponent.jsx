import styled from "styled-components";
import { Button, Dropdown, Form, Modal, ProgressBar } from "react-bootstrap";

import FileItemInList from "./FileItemInList";
import CustomCheckbox from "../atomComponents/CustomCheckbox";
import { connect } from "react-redux";

import { useState, setState } from "react";

import { updateDirList } from "../../reducers/DirListReducer";
import { updateDirs } from "../../reducers/SelectedDirReducer";


import CONFIG from '../../asset/config.json';
import axios from "axios";
import { ErrorCodes } from "../../modules/err/errorVariables";

const FileListComponent = (props) => {

    // Modal Events
    const [directoryAdderShow, setDirectoryAdderShow] = useState(false);
    const [fileUploaderShow, setFileUploaderShow] = useState(false);

    let allRootArr = decodeURI(window.location.pathname).split('/').slice(2); // url 파라미터로부터 가져온다
    
    // 공백 제거
    if(allRootArr[allRootArr.length - 1] == "") {
        allRootArr.pop();
    }


    let allRootArrToString = ""; // allRootArr를 화면에 출력하기 위해 String 변환
    let datas = []; // 파일리스트와 디렉토리 리스트를 저정하는 배열
    let selectedDirList = props.SelectedDirReducer.dirList;

    // 내 정보
    let userInfo = props.ConnectedUserReducer;

    // 체크박스 클릭 핸들러
    const checkBoxClickHandler = (f) => {

        // 각 파일의 체크박스 선택 시 사용되는 핸들러
        // 주로 선택된 파일 리스트를 redux를 사용해 관리하는데 사용한다.

        if(f["filename"] == ".." || f["filename"] == ".") {
            // 뒤로 가기 버튼 예외처리
            return;
        }

        let __key = f["filename"]+"/"+String(f["type"]);
        let targetIdx = selectedDirList.indexOf(__key);

        if(targetIdx > -1) {
            // 이미 있는 경우 해제해야 하므로
            // 삭제
            if(targetIdx == 0) {
                selectedDirList = selectedDirList.slice(1);
            } else {
                let leftArr = selectedDirList.slice(0, targetIdx);
                let rightArr = selectedDirList.slice(targetIdx + 1);
                selectedDirList = leftArr.concat(rightArr);
            }
            // 선택 리스트 수정 후
            // 결과 반영을 위한 redux 업데이트
            props.updateDirs(selectedDirList);
        } else {
            // 없는 경우 ==  파일 및 디렉토리 추가
            // 선택된 파일 리스트에 추가
            selectedDirList = selectedDirList.concat(__key);
            props.updateDirs(selectedDirList);
        }
    }

    // 디렉토리 생성 이벤트
    const createDirectoryEvent = async (e) => {
        let newDirectoryName = e.target.newDirectory.value;
        
        // 디렉토리명 검토
        if(newDirectoryName == "") {
            alert("생성할 디렉토리 이름을 입력하세요");
            e.preventDefault();
        }

        // 슬래시 있는 지 확인
        if(newDirectoryName.indexOf('/') != -1) {
            alert("디렉토리에 슬래시가 들어갈 수 없습니다.");
            return;
        } else {
            // 서버로부터 데이터를 받아요
            let token = userInfo.token;
            let staticId = userInfo.id;
            let targetRoot = allRootArr.join('/') + "/" + newDirectoryName;
            let URL = CONFIG.URL + "/server/storage/data/dir/" + staticId + "/" + targetRoot;

            axios.post(URL, null, {
                headers: { "Set-Cookie": token },
                withCredentials: true,
                crossDomain: true
            }).then((r) => {
                let data = r.data;
                if(data.code != 0) {
                    alert("디렉토리를 생성하는 데 문제가 발생했습니다.");
                }
            })

        }
        
    }

    // Start
    if(props.DirListReducer.errCode == undefined) {
        // 해당 디렉토리로부터 데이터를 서버로부터 갖고와서 업데이트
        props.updateDirList(allRootArr, userInfo.token, userInfo.id);

        // TODO: 로딩 페이지 디자인 필요
        return(
            <Layout>
                <h1>Loading</h1>
            </Layout>
        );
    } else if (props.DirListReducer.errCode != 0) {

        // 세션 만료로 인해 id가 소멸된 경우
        if(userInfo.id === undefined || userInfo.id == "")
            props.hisotory.push("/");
        
        alert("해당 디렉토리는 존재하지 않습니다.");
        props.history.goBack();
    }else {

        // 파일 리스트와 디렉토리 리스트를 전부 data에 저장
        datas = props.DirListReducer.directoryList.concat(props.DirListReducer.fileList);

        // List로 정의되어있는 루트를 문자열로 변환
        allRootArrToString = allRootArr.join('/');

        const FileItemsComponent = datas.map((f, index) => {

            let __color = ( (f['filename'] == '.' || f['filename'] == '..') ? '#FFFFFF': "#137813" )

            // Make File List Component
            return (
                <div key={index} style={{ display: "flex", marginBottom: "20px" }}>
                    <CustomCheckbox color={__color}
                            onClick={() => { checkBoxClickHandler(f); }} />
                    <FileItemInList 
                            isDir={f['isDir']}
                            filename={f['filename']}
                            fileType={f['type']} 
                            history={props.history} />
                </div>
            );

        });


        // Directory Upload Modal
        const DirectoryUploadModal = () => {

            const closeEvent = () => setDirectoryAdderShow(false);

            return (
                <Modal
                    show={directoryAdderShow}
                    onHide={closeEvent}
                    centered
                >
                    <Modal.Header closeButton>
                        <Modal.Title>디렉토리 생성</Modal.Title>
                    </Modal.Header>
                    <Form onSubmit={createDirectoryEvent}>
                        <Modal.Body>
                            <Form.Group className="mb-3" controlId="newDirectoryName">
                                <Form.Label>생성할 디렉토리 이름을 입력하세요</Form.Label>
                                <Form.Control type="text" placeholder="디렉토리 이름 입력" name="newDirectory" />
                            </Form.Group>
                        </Modal.Body>
                        <Modal.Footer>
                            <Button type="submit" variant="success">생성</Button>
                            <Button variant="secondary" onClick={closeEvent}>취소</Button>
                        </Modal.Footer>
                    </Form>
                </Modal>
            );
        }
        const FileUploadModal = () => {

            const closeEvent = () => setFileUploaderShow(false);

            const [uploadProcess, setUploadProcess] = useState({
                "targetFilesLength": -1,
                "uploadedFilesLength": -1,
                "progressFileName": undefined,
            });
            /*
                targetFilesLength: targetFiles의 길이
                
                uploadedFilesLength: 업로드 완료된 파일의 갯수
                    -1 => 시작 전
                    0 ~ ... => 업로드가 완료된 파일 갯수
                    선택된 파일 갯수와 일치 => 완료

                progressFileName: 업로드 진행 중인 파일의 이름
            */

            const uploadHandler = async (e) => {
                
                e.preventDefault();

                
                // 업로드 대상 파일 및 파일 갯수 저장
                let targetFiles = e.target.newUploadedFileList.files;
                let targetFilesLength = targetFiles.length;

                // 파일 업로드 진행바 생성을 위해 선택된 파일 갯수 갱신


                setUploadProcess({
                    "targetFilesLength": targetFilesLength,
                    "uploadedFilesLength": -1,
                    "progressFileName": undefined,
                })
                
                // 파일이 없는 경우
                if(targetFilesLength < 1) {
                    alert("파일을 선택해 주세요");
                    return;
                }

                // URL 생성
                let URL = `${CONFIG.URL}/server/storage/data/file/${props.ConnectedUserReducer.id}/${props.DirListReducer.curUrl.join('/')}`;

                // 업로드 시작
                setUploadProcess({
                    "targetFilesLength": targetFilesLength,
                    "uploadedFilesLength": 0,
                    "progressFileName": targetFiles[0].name
                });

                // 파일 순차적으로 업로드
                // filelist는 object가 아니기 때문에 For를 사용해야 한다
                for(let i = 0; i < targetFilesLength; i++) {
                    let file = targetFiles[i];
                    
                    //  URL 생성
                    let FILE_URL = `${URL}/${file.name}`;
                    
                    // 파일 업로드를 위한 FormData 생성
                    let formData = new FormData();
                    formData.append('file', file);


                    // 전송 시작
                    let result = await axios.post(FILE_URL, formData, {
                        headers: { 'Set-Cookie': props.ConnectedUserReducer.token},
                        withCredentials: true,
                        crossDomain: true
                    }).then((response) => response.data)
                    .catch((err) => {
                        // 전송 실패
                        return {
                            "code": ErrorCodes.ERR_AXIOS_FAILED,
                            "err": err
                        }
                    })

                    // 전송 결과
                    if(result.code == ErrorCodes.ERR_AXIOS_FAILED) {
                        // Axios Error: 주로 서버와 연결이 끊어졌을 때 발생한다.
                        alert("서버로부터 연결이 끊어졌습니다.");
                        break;
                    } else if(result.code == 0) {

                        // 전송 성공
                        let nextFileName = undefined;
                        if(i == targetFilesLength - 1) {
                            nextFileName = "업로드 완료"
                        } else {
                            nextFileName = targetFiles[i + 1].name;
                        }

                        setUploadProcess({
                            "targetFilesLength": targetFilesLength,
                            "uploadedFilesLength": i + 1,
                            "progressFileName": nextFileName,
                        });
                    } else {
                        // 서버상의 에러
                        alert("파일에 문제가 있습니다. 다시 업로드해 주세요");
                        break;
                    }
                    
                }
            }

            const ModalBodyComponent = () => {
                // 업로드 진행 상태에 따라 내용도 달라져야 한다
                
                if(uploadProcess.uploadedFilesLength == -1) {
                    // 업로드 시작 전
                    return (
                        <Modal.Body>
                            <Form.Group className="mb-3" controlId="newUploadedFileName">
                                <Form.Label>업로드 할 파일을 선택해 주세요</Form.Label>
                                <Form.Control type="file" name="newUploadedFileList" multiple />
                            </Form.Group>
                        </Modal.Body>
                    );
                } else {
                    // 업로드 진행
                    let percentage = (uploadProcess.uploadedFilesLength / uploadProcess.targetFilesLength) * 100;
                    // 진행 상황 Percentage


                    return (
                        <Modal.Body>
                            <h5>Upload: {uploadProcess.progressFileName}</h5>
                            <ProgressBar striped variant="success" now={percentage} />
                        </Modal.Body>
                    );
                }
            }
            const ModalFooterComponent = () => {

                // 업로드 진행 상태에 따라 버튼 이벤트도 달라진단다
                if(uploadProcess.uploadedFilesLength == -1) {
                    // 업로드 전
                    return (
                        <Modal.Footer>
                            <Button variant="success" type="submit">업로드</Button>
                            <Button variant="secondary" onClick={closeEvent}>취소</Button>
                        </Modal.Footer>
                    );
                } else if (uploadProcess.progressFileName !== undefined && 
                    uploadProcess.uploadedFilesLength < uploadProcess.targetFilesLength) {
                    // 진행중
                    return (
                        <Modal.Footer />
                    );
                } else {
                    // 업로드 완료
                    return (
                        <Modal.Footer>
                            <Button variant="success" onClick={() => {
                                window.location.reload();
                            }}>확인</Button>
                        </Modal.Footer>
                    );
                }
            }
            
            return (<Modal
                show={fileUploaderShow}
                onHide={() => {
                    if(uploadProcess.uploadedFilesLength == uploadProcess.targetFilesLength &&
                        uploadProcess.progressFileName !== undefined) {
                            // 업로드 완료 시 새로고침
                            window.location.reload();
                    } else {
                        closeEvent();
                    }
                    
                }}
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title>파일 업로드</Modal.Title>
                </Modal.Header>
                <Form onSubmit={uploadHandler}>
                    <ModalBodyComponent />
                    <ModalFooterComponent />
                </Form>
            </Modal>);
        }


        // Component Render
        return (
            <Layout>
                <h4 style={{ fontWeight: "bold" }}>{allRootArrToString}</h4>
                
                <div style={{ marginTop: "20px", display: "flex" }}>

                    <Dropdown>
                        <Dropdown.Toggle variant="success" id="item-adder" style={{ paddingLeft: "30px", paddingRight: "30px", marginRight: "10px" }}>
                            업로드
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item onClick={() => setFileUploaderShow(true)}>파일 업로드</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>

                    <Dropdown>
                        <Dropdown.Toggle variant="outline-success" id="item-adder">
                            생성
                        </Dropdown.Toggle>
    
                        <Dropdown.Menu>
                            <Dropdown.Item onClick={() => setDirectoryAdderShow(true)}>디렉토리 생성</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>

                </div>
    
                <div style={{ backgroundColor: "gray", width: "100%", height:"1.4px", marginTop: "20px", marginBottom: "20px" }} />
                <ListLayout>
                    {FileItemsComponent}
                </ListLayout>

                <DirectoryUploadModal />
                <FileUploadModal />
            </Layout>
        );
    }
}
const mapStateToProps = (state) => {
    return {
        "DirListReducer": state.DirListReducer,
        "SelectedDirReducer": state.SelectedDirReducer,
        "ConnectedUserReducer": state.ConnectedUserReducer
    }
}

export default connect(mapStateToProps, {
    updateDirList, updateDirs
})(FileListComponent);

const Layout = styled.div`
    line-height: 0.4em;

    font-family: "Gothic A1";
    width: 65%;
    height: 100vh;

    border: 1.2px solid #1DB21D;
    box-shadow: 2px 2px 3px gray;

    padding: 30px;
`;
const ListLayout = styled.div`

    overflow: scroll;
    height: 70%;
    
    &::-webkit-scrollbar {
        width: 6px;
        height: 6px;

        border-radius: 6px;
        background: rgba(255 255, 255, 0.4);
    }
    &::-webkit-scrollbar-thumb {
        background-color: rgba(19, 120, 19, 0.4);
        border-radius: 6px;
    }
    
`