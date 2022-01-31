import styled from 'styled-components';
import { ResponsiveQuery } from '../../variables/responsive';
import { useMediaQuery } from 'react-responsive';

// icons
import IconDirectory from '../../asset/img/icon-directory.svg';
import IconNormalFile from '../../asset/img/icon-normalfile.svg';
import { Colors } from '../../variables/color';
import TableRawComponent from './TableRawComponent';

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
            return <TableRawComponent 
                fileName={d['name']} fileType={d['file-type']}
                createDate={d['create-date']} fileSize={d['size']}
            /> 
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

export default DataLayout;