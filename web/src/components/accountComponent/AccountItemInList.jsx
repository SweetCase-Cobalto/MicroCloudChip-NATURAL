import { useState } from "react";
import { Image } from "react-bootstrap";
import { connect } from "react-redux";
import { selectUser } from "../../reducers/SelectedAccountReducer";

const AccountItemInList = (props) => {
    /*
        계정 관리 페이지에서
        사용되는 계정 컴포넌트
    */

    const [isHovered, setIsHovered] = useState(false);

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
                <Image src={props.imgLink} alt="userimg" width="110px" height="110px" roundedCircle />
                <h5 style={{ marginTop: "40px" }}>{props.username}</h5>
            </center>
        </div>
    );
}

const mapStateToProps = (state) => {
    return state.SelectedAccountReducer;
};
export default connect(mapStateToProps, {selectUser})(AccountItemInList);