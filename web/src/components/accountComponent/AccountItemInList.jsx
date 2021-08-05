import { useState } from "react";
import { Image } from "react-bootstrap";

const AccountItemInList = (props) => {

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
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}>
            <center style={{ paddingTop: "20px" }}>
                <Image src={props.imgLink} alt="userimg" width="110px" height="110px" roundedCircle />
                <h5 style={{ marginTop: "40px" }}>{props.username}</h5>
            </center>
        </div>
    );
}
export default AccountItemInList;