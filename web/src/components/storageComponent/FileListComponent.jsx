import styled from "styled-components";
import { Button, Dropdown, Form, Modal } from "react-bootstrap";

import FileItemInList from "./FileItemInList";
import CustomCheckbox from "../atomComponents/CustomCheckbox";
import { connect } from "react-redux";

import { useState } from "react";

import { updateDirList } from "../../reducers/DirListReducer";
import { updateDirs } from "../../reducers/SelectedDirReducer";

const FileListComponent = (props) => {
    const [directoryAdderShow, setDirectoryAdderShow] = useState(false);

    let allRootArr = window.location.pathname.split('/').slice(2); // url 파라미터로부터 가져온다
    let allRootArrToString = ""; // allRootArr를 화면에 출력하기 위해 String 변환
    let datas = []; // 파일리스트와 디렉토리 리스트를 저정하는 배열
    let selectedDirList = props.SelectedDirReducer.dirList;

    // 체크박스 클릭 핸들러
    const checkBoxClickHandler = (f) => {

        // 각 파일의 체크박스 선택 시 사용되는 핸들러
        // 주로 선택된 파일 리스트를 redux를 사용해 관리하는데 사용한다.

        let __key = f["filename"]+"/"+String(f["file-type"]);
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

    // Start
    if(props.DirListReducer.curUrl.length == 0) {

        // 해당 디렉토리로부터 데이터를 서버로부터 갖고와서 업데이트
        props.updateDirList(allRootArr);

        // TODO: 로딩 페이지 디자인 필요
        return(
            <Layout>
                <h1>Loading</h1>
            </Layout>
        );
    } else {

        // 파일 리스트와 디렉토리 리스트를 전부 data에 저장
        datas = props.DirListReducer.fileList.concat(props.DirListReducer.directoryList);

        // List로 정의되어있는 루트를 문자열로 변환
        allRootArrToString = allRootArr.join('/');

        const FileItemsComponent = datas.map((f, index) => {
            // Make File List Component
            return (
                <div key={index} style={{ display: "flex", marginBottom: "20px" }}>
                    <CustomCheckbox color="#137813" 
                                    onClick={() => { checkBoxClickHandler(f); }} />
                    <FileItemInList 
                            isDir={f['isDir']}
                            filename={f['filename']}
                            fileType={f['file-type']} />
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
                >
                    <Modal.Header closeButton>
                        <Modal.Title>디렉토리 생성</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form>
                            <Form.Group className="mb-3" controId="newDirectoryName">
                                <Form.Label>생성할 디렉토리 이름을 입력하세요</Form.Label>
                                <Form.Control type="text" placeholder="디렉토리 이름 입력" />
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="success">생성</Button>
                        <Button variant="secondary" onClick={closeEvent}>취소</Button>
                    </Modal.Footer>
                </Modal>
            );
        }

        return (
            <Layout>
                <h4 style={{ fontWeight: "bold" }}>{allRootArrToString}</h4>
                
                <div style={{ marginTop: "20px", display: "flex" }}>

                    <Dropdown>
                        <Dropdown.Toggle variant="success" id="item-adder" style={{ paddingLeft: "30px", paddingRight: "30px", marginRight: "10px" }}>
                            업로드
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item>파일 업로드</Dropdown.Item>
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
                <div>
                    {FileItemsComponent}
                </div>

                <DirectoryUploadModal />
            </Layout>
        );
    }
}
const mapStateToProps = (state) => {
    // return state.DirListReducer;
    return {
        "DirListReducer": state.DirListReducer,
        "SelectedDirReducer": state.SelectedDirReducer,
    }
}

export default connect(mapStateToProps, {
    updateDirList, updateDirs
})(FileListComponent);

const Layout = styled.div`
    line-height: 0.4em;

    font-family: "Gothic A1";
    width: 65%;

    border: 1.2px solid #1DB21D;
    box-shadow: 2px 2px 3px gray;

    padding: 30px;
`;