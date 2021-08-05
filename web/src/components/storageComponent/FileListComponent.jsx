import styled from "styled-components";
import { Button, Dropdown } from "react-bootstrap";

import FileItemInList from "./FileItemInList";
import CustomCheckbox from "../atomComponents/CustomCheckbox";
import { connect } from "react-redux";

import { updateDirList } from "../../reducers/DirListReducer";
import { updateDirs } from "../../reducers/SelectedDirReducer";

const FileListComponent = (props) => {
    
    let allRootArr = window.location.pathname.split('/').slice(2); // url 파라미터로부터 가져온다
    let allRootArrToString = "";
    let datas = [];
    let selectedDirMap = new Map();

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

        
        // Data를 이용해 선택 파일 리스트 생성
        if(props.SelectedDirReducer.dirListMap === undefined) {
            // reducer에 데이터가 없을 경우
            // datas 를 이용해 갱신
            datas.map((f) =>{
                selectedDirMap.set(f["filename"]+"/"+String(f["isDir"]), false);
            });

            props.updateDirs(selectedDirMap);
            // FIXME: ReactJS에서 안티패턴으로 인한 warning이 발생하나 정상적으로 작동
            // 안티패턴을 피하기 위한 방법 조사 필요
        } else {
            // 존재한다면
            // local variable에 reducer data 동기화
            selectedDirMap = props.SelectedDirReducer.dirListMap;
        }

        // List로 정의되어있는 루트를 문자열로 변환
        allRootArrToString = allRootArr.join('/');

        const FileItemsComponent = datas.map((f, index) => {
            // Make File List Component
            return (
                <div key={index} style={{ display: "flex", marginBottom: "20px" }}>
                    <CustomCheckbox color="#137813" 
                                    onClick={() => {
                                        let __key = f["filename"]+"/"+String(f["isDir"]);
                                        selectedDirMap.set(__key, !selectedDirMap.get(__key));
                                        props.updateDirs(selectedDirMap);
                                    }} />
                    <FileItemInList 
                            isDir={f['isDir']}
                            filename={f['filename']}
                            fileType={f['file-type']} />
                </div>
            );
        });
        return (
            <Layout>
                <h4 style={{ fontWeight: "bold" }}>{allRootArrToString}</h4>
                
                <div style={{ marginTop: "20px", display: "flex" }}>
                    <Button variant="success" style={{ marginRight: "20px", padding: "0px 30px 0px 30px" }}>업로드</Button>
                    <Dropdown>
                        <Dropdown.Toggle variant="outline-success" id="item-adder">
                            생성
                        </Dropdown.Toggle>
    
                        <Dropdown.Menu>
                            <Dropdown.Item onClick={e => {console.log(e)}}>디렉토리 생성</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                </div>
    
                <div style={{ backgroundColor: "gray", width: "100%", height:"1.4px", marginTop: "20px", marginBottom: "20px" }} />
                <div>
                    {FileItemsComponent}
                </div>
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