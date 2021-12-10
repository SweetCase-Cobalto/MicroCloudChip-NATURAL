import styled from 'styled-components';
import { Colors } from '../variables/color';

import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';

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

    const isPC = useMediaQuery(ResponsiveQuery.PC);
    const isMobile = useMediaQuery(ResponsiveQuery.MOBILE);
    const isTablet = useMediaQuery(ResponsiveQuery.TABLET);
    const ContentsComponent = () => (
        <div>
            <Item name="My Storage" />
            <Item name="Accounts" />
            <Item name="Settings" />
        </div>
    );

    return (
        <div>
            {isPC && <Layout><ContentsComponent /></Layout>}
            { (isMobile || isTablet) && <MobileLayout><ContentsComponent /></MobileLayout>}
        </div>
    );
}

const Layout = styled.div`
    width: 240px;
    height: 94vh;
    background-color: ${Colors.LEFT_MENU_BAR_COLOR};
    color: ${Colors.ACCESS_COLOR};
    
    padding-top: 40px;
    padding-left: 20px;
`
const MobileLayout = styled.div`
    width: 240px;
    height: 100vh;
    background-color: ${Colors.LEFT_MENU_BAR_COLOR};
    color: ${Colors.ACCESS_COLOR};

    padding-top: 40px;
    padding-left: 20px;
`

export default LeftMenuBar;