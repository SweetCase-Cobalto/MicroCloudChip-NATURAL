import { Dropdown } from "react-bootstrap";
import { useState } from "react";

const BootstrapDropdownSelector = (props) => {
    let itemList = props.itemList;
    const [selectedItem, setSelectedItem] = useState(itemList[0]);

    const ItemComponents = itemList.map((item, idx) => 
        <Dropdown.Item key={idx} eventKey={item} onSelect={e => {
            setSelectedItem(e);
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