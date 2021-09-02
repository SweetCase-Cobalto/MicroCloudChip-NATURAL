// Icons
import dirImg from '../../asset/img/icons/dir.svg';
import audioFileImg from '../../asset/img/icons/audio-file.svg';
import exeFileImg from '../../asset/img/icons/exe-file.svg';
import imgFileImg from '../../asset/img/icons/img-file.svg';
import pdfFileImg from '../../asset/img/icons/pdf-file.svg';
import txtFileImg from '../../asset/img/icons/txt-file.svg';
import otherFileImg from '../../asset/img/icons/unknown-file.svg';
import videoFileImg from '../../asset/img/icons/video-file.svg';


import { useState } from "react";
import { connect } from "react-redux";

const FileItemInList = (props) => {
    /*
        파일 및 디렉토리 아이템 컴포넌트
    */

    /*
        props info
        filename: String
        isDir: bool
        fileType: dir, text, exe, pdf, image, audio, video, other, none
    */
   const [isMouseEntered, setIsMouseEntered] = useState(false);
   let filename = props.filename;
   let isDir = props.isDir;
   let fileType = props.fileType;

   const onClickEvent = () => {
       if(isDir) {
           // 디렉토링 경우
           // 해당 루트로 이동
           let curUrl = props.curUrl;
           let nextUrlToString = curUrl.join('/') + "/" + filename;
           window.location.assign("/storage/"+nextUrlToString);
       } else {
           // TODO: 파일 다운로드
           // TODO: 차기 버전은 특정 타입에 따라 다른 작업을 수행해야 함
       }
   }

   const FileImgLayer = () => {
        // 이미지 태그
        // TODO: 이미지 Url 갖고오는 거 언젠간 모듈화 할예정
        let imgLink = "";
        
        if(isDir) {
            imgLink = dirImg;
        } else {
            fileType = fileType.toLowerCase();
            switch(fileType) {
                case 'text': imgLink = txtFileImg; break;
                case 'execute': imgLink = exeFileImg; break;
                case 'pdf': imgLink = pdfFileImg; break;
                case 'image': imgLink = imgFileImg; break;
                case 'audio': imgLink = audioFileImg;  break;
                case 'video': imgLink = videoFileImg; break;
                case 'other': imgLink = otherFileImg; break;
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
        <div style={{ width: "100%"}}>   
            <div style={{ display: "flex" }}>
                <FileImgLayer />
                <h5 style={{ 
                        paddingTop: "5px", 
                        cursor: "pointer", 
                        textDecoration: isMouseEntered ? "underline" : "none"
                    }}
                    onClick={onClickEvent} 
                    onMouseEnter={e => { setIsMouseEntered(true)}} 
                    onMouseLeave={e => { setIsMouseEntered(false)}}
                >{filename}</h5>
            </div>
            <div style={{ borderBottom: "1px solid gray"}} />
        </div>
   );
}
const mapStateProps = (state) => {
    return state.DirListReducer;
}
export default connect(mapStateProps)(FileItemInList);