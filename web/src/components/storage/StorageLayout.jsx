import styled from 'styled-components';
import { ResponsiveQuery } from '../../variables/responsive';
import { useMediaQuery } from 'react-responsive';
import { Colors } from '../../variables/color';
import RootTag from './RootTag';

const StorageLayout = () => {
    
    const isPC = useMediaQuery(ResponsiveQuery.PC);
    const isTablet = useMediaQuery(ResponsiveQuery.TABLET);
    const isMobile = useMediaQuery(ResponsiveQuery.MOBILE);

    // Test Data for UI Test
    const root = ["explore", "win32", "win6", "아까처럼 말이지", "that is the document onthe world"]


    // 컴포넌트 생성
    const RootComponent = root.map((r, idx) => <RootTag name={r} key={idx} />);


    return (
        <Layout>

            <div>
                { isPC && 
                    <TitleLayoutPC>
                        <h1 style={{ color: Colors.COLORED_BOLD_COLOR, marginBottom: "30px" }}><strong>Storage</strong></h1>
                        <TagLayout>{RootComponent}</TagLayout>
                    </TitleLayoutPC>
                }
                { isTablet &&
                    <TitleLayoutTablet>
                        <h1 style={{ color: Colors.COLORED_BOLD_COLOR, marginBottom: "30px"}}><strong>Storage</strong></h1>
                        <TagLayout>{RootComponent}</TagLayout>
                    </TitleLayoutTablet>
                }
                { isMobile && 
                    <TitleLayoutMobile>
                        <h1 style={{ color: Colors.COLORED_BOLD_COLOR, marginBottom: "20px" }}><strong>Storage</strong></h1>
                        <TagLayout>{RootComponent}</TagLayout>
                    </TitleLayoutMobile>
                }
                
            </div>
            
            <div style={{ width: "100%", height: "1px", background: "gray" }} />
        </Layout>
    );
}

const Layout = styled.div`
    width: 100%;
`
const TitleLayoutPC = styled.div`
    padding: 80px 20px 20px 60px;
`
const TitleLayoutTablet = styled.div`
    padding: 50px 30px 20px 30px;
`
const TitleLayoutMobile = styled.div`
    padding: 30px 30px 20px 40px;
`
const TagLayout = styled.div`
    display: flex;
    flex-wrap: wrap;
`


export default StorageLayout;