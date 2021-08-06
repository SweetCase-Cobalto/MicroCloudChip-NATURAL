import { useState } from "react"

// 부트스트랩 체크박스 별로라 직접 만듦

const CustomCheckbox = (props) => {
    const [isSelected, setIsSelected] = useState(false);
    let color = props.color;
    const cssBorder = "2px solid " + color;

    let styleData = {
        border: cssBorder,
        width: "30px",
        height: "30px",
        marginRight: "15px",
        cursor: "pointer",
        backgroundColor: "white"
    }
    if(isSelected) {
        styleData['backgroundColor'] = color;
    }
    return  (
        <div style={styleData} onClick={(e) => {
            setIsSelected(!isSelected);
            
            // If have onClick Event
            if(props.onClick !== undefined) {
                props.onClick();
            }
        }} />
    );
}
export default CustomCheckbox;