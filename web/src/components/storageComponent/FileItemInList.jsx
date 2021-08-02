import styled from "styled-components";

// Icons
import dirImg from '../../asset/img/icons/dir.svg';
import audioFileImg from '../../asset/img/icons/audio-file.svg';
import exeFileImg from '../../asset/img/icons/exe-file.svg';
import imgFileImg from '../../asset/img/icons/img-file.svg';
import pdfFileImg from '../../asset/img/icons/pdf-file.svg';
import txtFileImg from '../../asset/img/icons/txt-file.svg';
import otherFileImg from '../../asset/img/icons/unknown-file.svg';
import videoFileImg from '../../asset/img/icons/video-file.svg';

const FileItemInList = (props) => {
    
    /*
        props info
        filename: String
        isDir: bool
        fileType: text, exe, pdf, image, audio, video, other, none
    */
   let filename = props.filename;
   let isDir = props.isDir;
   let fileType = props.fileType;

   const FileImgLayer = () => {
        // 이미지 태그
        let imgLink = "";
        
        if(isDir) {
            imgLink = dirImg;
        } else {
            switch(fileType) {
                case 'text': imgLink = txtFileImg; break;
                case 'exe': imgLink = exeFileImg; break;
                case 'pdf': imgLink = pdfFileImg; break;
                case 'image': imgLink = imgFileImg; break;
                case 'audio': imgLink = audioFileImg;  break;
                case 'video': imgLink = videoFileImg; break;
                case 'none': imgLink = otherFileImg; break;
                default: imgLink = otherFileImg; break;
            }
        }

        return (
            <div style={{ paddingBottom: "10px", marginRight: "10px" }}>
                <img src={imgLink} width="30px" height="30px" />
            </div>
        );
   }

   return (
        <div style={{ width: "100%" }} >   
            <div style={{ display: "flex" }}>
                <FileImgLayer />
                <h5 style={{ paddingTop: "5px" }}>{filename}</h5>
            </div>
            <div style={{ borderBottom: "1px solid gray"}} />
        </div>
   );
}
export default FileItemInList;

const Layer = styled.div`
    width: 100%;
    height: 50px;
`;