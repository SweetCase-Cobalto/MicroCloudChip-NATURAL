import styled from "styled-components";
import { Button, Dropdown } from "react-bootstrap";

const FileListComponent = (props) => {

    let allRootArr = props.allRootArr;
    return (
        <Layout>
            <h3 style={{ fontWeight: "bold" }}>{allRootArr}</h3>
            
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

            <div style={{ backgroundColor: "gray", width: "100%", height:"1px", marginTop: "20px", marginBottom: "20px" }} />
        </Layout>
    );
}
export default FileListComponent;

const Layout = styled.div`
    line-height: 0.4em;

    font-family: "Gothic A1";
    width: 65%;
    height: 100vh;

    border: 1.2px solid #1DB21D;
    box-shadow: 2px 2px 3px gray;

    padding: 30px;
`;