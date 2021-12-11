import styled from "styled-components";

import { Colors } from "../../variables/color";

import { ResponsiveQuery } from '../../variables/responsive';
import { useMediaQuery } from 'react-responsive';

// Storage에서 root 표시할 때 사용
const RootTag = (props) => {

    const isPC = useMediaQuery(ResponsiveQuery.PC);
    const isTablet = useMediaQuery(ResponsiveQuery.TABLET);
    const isMobile = useMediaQuery(ResponsiveQuery.MOBILE);

    const name = props.name;    // 파일 이름

    return (
        <Layout>
            {(isPC || isTablet) && <PCLayout>
                <strong>{ name }</strong>
            </PCLayout>}
            {
                (isMobile) && <MobileLayout>
                    <strong>{ name }</strong>
                </MobileLayout>
            }
        </Layout>
    );
}


const Layout = styled.div`
    background: ${Colors.LIGHT_ACCESS_COLOR};
    color: ${Colors.ROOT_TAG_COLOR};
    border: 1.5px solid ${Colors.ROOT_TAG_COLOR};
    border-radius: 7px;
    margin-right: 10px;
    margin-bottom: 5px;
    font-size: 0.8em;
`
const PCLayout = styled.div`
    padding 5px 10px 5px 10px;
`
const MobileLayout = styled.div`
    padding 3px 7px 3px 7px;
    font-size: 0.7em;
`

export default RootTag;