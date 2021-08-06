import { Dropdown } from "react-bootstrap";
import { useState } from "react";

const BootstrapDropdownSelector = (props) => {
    
    /* 
        부트스트랩 드롭다운 개조형
        항목을 선택하면 선택한 항목이 출력되게 수정
    */
    let itemList = props.itemList; // 드롭다운 아이템 리스트
    // + 항목을 선택했을 때 반응하는 함수인 onChangedEvent도 param으로 등록해야 한다.

    const [selectedItem, setSelectedItem] = useState(itemList[0]);

    const ItemComponents = itemList.map((item, idx) => 
        <Dropdown.Item key={idx} eventKey={item} onSelect={e => {
            setSelectedItem(e);

            // onChangedEvent --> 사용자 지정 함수
            // 해당 함수의 param은 선택된 아이템
            props.onChangedEvent(e);
        }}>{item}</Dropdown.Item>
    );

    return (
        <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
                {selectedItem}
            </Dropdown.Toggle>

            <Dropdown.Menu>
                {ItemComponents}
            </Dropdown.Menu>
        </Dropdown>
    );
}

export default BootstrapDropdownSelector;