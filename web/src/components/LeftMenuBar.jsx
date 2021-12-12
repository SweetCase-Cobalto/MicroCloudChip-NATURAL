import styled from 'styled-components';
import { Colors } from '../variables/color';
import { Link } from  'react-router-dom';
import React from 'react';

import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';

const Item = (props) => {

    return (
        <ItemLayout>
            <h5>{props.name}</h5>
        </ItemLayout>
    );

}

const LeftMenuBar = () => {
    // 왼쪽 메뉴 바임

    const isPC = useMediaQuery(ResponsiveQuery.PC);
    const isMobile = useMediaQuery(ResponsiveQuery.MOBILE);
    const isTablet = useMediaQuery(ResponsiveQuery.TABLET);

    const ContentsComponent = () => (
        <div>
            <Link to="/storage" style={{ textDecoration: "none", color: `${Colors.ACCESS_COLOR}` }}><Item name="My Storage" /></Link>
            <Link to="/account" style={{ textDecoration: "none", color: `${Colors.ACCESS_COLOR}` }}><Item name="Accounts" /></Link>
            <Link to="/settings" style={{ textDecoration: "none", color: `${Colors.ACCESS_COLOR}` }}><Item name="Settings" /></Link>
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
    color: ${(Colors.ACCESS_COLOR)};

    padding-top: 40px;
    padding-left: 20px;
`

const ItemLayout  = styled.div`
    padding-top: 5px;
    padding-bottom: 5px;
    &:hover {
        background-color: #CBCBCB;
    }
`
export default LeftMenuBar;