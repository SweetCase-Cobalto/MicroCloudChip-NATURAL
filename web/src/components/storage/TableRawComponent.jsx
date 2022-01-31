import styled from 'styled-components';
import IconDirectory from '../../asset/img/icon-directory.svg';
import IconNormalFile from '../../asset/img/icon-normalfile.svg';
import { Colors } from '../../variables/color';
import React from 'react';


const TableRawComponent = (props) => {

    const createDate = props.createDate;
    const fileType = props.fileType;
    const fileName = props.fileName;
    const fileSize = props.fileSize;

    
    const FileImgComponent = () => {
        // 파일/디렉토리 아이콘
        if(fileType == 'dir') {
            return <img src={IconDirectory} height="20px" alt="dir" style={{ marginRight: "5px" }} />
        } else {
            return <img src={IconNormalFile} height="20px" alt="dir" style={{ marginRight: "5px" }} />
        }
    }

    return (
        <Layer>
            <th scope="row" style={{ 
                    display: "flex", flexWrap: "wrap", 
                    marginTop: "10px", marginBottom: "10px"}}>
                <FileImgComponent /> {fileName}
            </th>
            <td>{createDate}</td>
            <td>{fileSize}</td>
        </Layer>
    );
}

const Layer = styled.tr`
    &:hover {
        background-color: ${Colors.ITEM_SELECTED_COLOR};
    }
`

export default TableRawComponent;