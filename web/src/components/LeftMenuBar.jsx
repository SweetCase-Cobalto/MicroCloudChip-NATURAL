import styled from 'styled-components';
import { Colors } from '../variables/color';

const Item = (props) => {

    return (
        <div style={{
            paddingBottom: "10px"
        }}>
            <h5>{props.name}</h5>
        </div>
    );
}

const LeftMenuBar = () => {
    // 왼쪽 메뉴 바임
    return (
        <Layout>
            <div>
                <Item name="My Storage" />
                <Item name="Accounts" />
                <Item name="Settings" />
            </div>
        </Layout>
    );
}

const Layout = styled.div`
    width: 240px;
    height: 100%;
    background-color: ${Colors.LEFT_MENU_BAR_COLOR};
    color: ${Colors.ACCESS_COLOR};
    
    padding-top: 40px;
    padding-left: 20px;
`

export default LeftMenuBar;