import { useState } from "react";
import { Image } from "react-bootstrap";
import { connect } from "react-redux";
import { selectUser } from "../../reducers/SelectedAccountReducer";
import defaultIconImg from '../../asset/img/icons/user-icon.svg';
import { cookieRequestedImgUrlToAvailableUrl } from '../../modules/tool/cookieRequestedImgUrlToAvailableUrl';

const AccountItemInList = (props) => {
    /*
        계정 관리 페이지에서
        사용되는 계정 컴포넌트
    */

    const [isHovered, setIsHovered] = useState(false);
    const [realImgUrl, setRealImgUrl] = useState(undefined);
    

    const ImgComponent = () => {
        // 리스트에 출력될 이미지 컴포넌트
        if(realImgUrl == undefined) {
            
            // Get Data
            if(props.imgLink == defaultIconImg) {
                // 기존 이미지(해당 유저의 프로필 이미지가 없는 경우)
                setRealImgUrl(defaultIconImg);
            } else {
                // 있는 경우
                cookieRequestedImgUrlToAvailableUrl(props.imgLink, props.connected.token)
                .then((url) => { setRealImgUrl(url); })
            }
            return <Image style={{backgroundColor: "gray"}} alt="userimg" width="110px" height="110px" roundedCircle />
        } else {
            return <Image src={realImgUrl} alt="userimg" width="110px" height="110px" roundedCircle />
        }
    }

    return (
        <div style={{
            padding: "10px",
            border: "1px gray solid",
            width: "180px",
            height: "240px",
            cursor: "pointer",
            borderRadius: "20px",
            backgroundColor: isHovered ? "#e7f7e1" : "white"
            
        }}
        onClick={() => {
            // 선택 계정 변경
            // AccoutnStateComponent에 적용이 되며
            // 계정 삭제 및 변경이 가능해짐
            props.selectUser(props.staticId);
        }}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}>
            <center style={{ paddingTop: "20px" }}>
                <ImgComponent />
                <h5 style={{ marginTop: "40px" }}>{props.username}</h5>
            </center>
        </div>
    );
}

const mapStateToProps = (state) => {
    return {
        "selected": state.SelectedAccountReducer,
        "connected": state.ConnectedUserReducer
    }
};
export default connect(mapStateToProps, {selectUser})(AccountItemInList);