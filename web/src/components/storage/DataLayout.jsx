import styled from 'styled-components';
import { ResponsiveQuery } from '../../variables/responsive';
import { useMediaQuery } from 'react-responsive';

// icons
import IconDirectory from '../../asset/img/icon-directory.svg';
import IconNormalFile from '../../asset/img/icon-normalfile.svg';
import { Colors } from '../../variables/color';

import '../../asset/css/customButton.css';
import React from 'react';

const DataLayout = () => {
    // Storage에서 파일 및 디렉토리 내역 볼 때 사용

    const isPC = useMediaQuery(ResponsiveQuery.PC);
    const isTablet = useMediaQuery(ResponsiveQuery.TABLET);
    const isMobile = useMediaQuery(ResponsiveQuery.MOBILE);


    // 스토리지 데이터 (테스트용)
    const storageDataForTest = [
        {"file-type": "dir", "name": "Directory 1", "create-date": "2021-01-01 10:01:01", "size": "4 Files", "shared": "Unable"},
        {"file-type": "dir", "name": "Directory 2", "create-date": "2021-01-01 10:01:01", "size": "1 File", "shared": "Unable"},
        {"file-type": "dir", "name": "Directory 3", "create-date": "2021-01-01 10:01:01", "size": "434 Files", "shared": "Unable"},
        {"file-type": "dir", "name": "Directory 4", "create-date": "2021-01-01 10:01:01", "size": "412 Files", "shared": "Unable"},

        
        {"file-type": "file", "name": "File1", "create-date": "2021-01-01 10:01:01", "size": "1 KB", "shared": "shared"},
        {"file-type": "file", "name": "File2", "create-date": "2021-01-01 10:01:01", "size": "123.43 MB", "shared": "not-shared"},


    ]

    const ConsoleControlComponent = () => {
        // 버튼들모임
        return (
            <div style={{ dispaly: "flex", flexWrap: "wrap", paddingBttom: "30px" }}>
                <button className="custombutton-access" style={{ marginRight: "20px", marginBottom: "5px" }}>Upload</button>
                <button className="custombutton-access" style={{ marginRight: "20px", marginBottom: "5px" }}>New Directory</button>
                <button className="custombutton-access-out" style={{ marginRight: "20px", marginBottom: "5px" }}>Change Name</button>
                <button className="custombutton-danger-out" style={{ marginRight: "20px", marginBottom: "5px" }}>Delete</button>
            </div>
        )
    }

    const DataTable = () => {
        // 데이터테이블
        
        const DataComponent = storageDataForTest.map((d, idx) => {

            const SharedBtn = () => {
                // 공유 상태에 따른 다른 버튼 생성
                if(d['shared'] == 'shared') {
                    return <button className='custombutton-access' style={{ 
                        fontSize: "0.7em"
                    }}>Shared</button>
                } else if(d['shared'] == 'not-shared') {
                    return <button className="custombutton-danger" style={{ 
                        fontSize: "0.7em"
                    }}>Not Shared</button>
                } else {
                    return <button className="custombutton-unable" style={{ 
                        fontSize: "0.7em"
                    }} disabled>Unable</button>
                }
            }
            
            const FileImgComponent = () => {
                // 파일/디렉토리 아이콘
                if(d['file-type'] == 'dir') {
                    return <img src={IconDirectory} height="20px" alt="dir" style={{ marginRight: "5px" }} />
                } else {
                    return <img src={IconNormalFile} height="20px" alt="dir" style={{ marginRight: "5px" }} />
                }
            }
            

            return (<TableRawComponent key={idx}>
                <th scope="row" style={{ 
                    display: "flex", flexWrap: "wrap", 
                    marginTop: "10px", marginBottom: "10px"}}><FileImgComponent /> {d['name']}</th>
                <td >{d['create-date']}</td>
                <td>{d['size']}</td>
                <td><SharedBtn /></td>
            </TableRawComponent>);
        })

        return (
            <table style={{ 
                    margin: "20px 20px 20px 20px", 
                    width: "100%",
                }}>
                <thead style={{
                    borderBottom: "1px solid gray",
                }}>
                    <tr>
                        <th scope="col" style={{ paddingBottom: "10px" }}>Name</th>
                        <th scope="col">Create Date</th>
                        <th scope="col">Size</th>
                        <th scope="col">Shared</th>
                    </tr>
                </thead>
                <tbody>
                    {DataComponent}
                </tbody>
            </table>
        )
    }

    const paddingRightValue = () => {
        if(isPC) return "200px";
        else if(isTablet) return "60px";
        else return "30px";
    }

    return (
        <div style={{ paddingRight: `${paddingRightValue()}` }}>
            <ConsoleControlComponent />
            <DataTable />
        </div>
    );
}

// 마우스 올려놓으면 색깔 변함
const TableRawComponent = styled.tr`
    &:hover {
        background-color: ${Colors.ITEM_SELECTED_COLOR};
    }
`
export default DataLayout;