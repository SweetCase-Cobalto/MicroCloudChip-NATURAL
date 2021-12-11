import styled from 'styled-components';
import { ResponsiveQuery } from '../../variables/responsive';
import { useMediaQuery } from 'react-responsive';
import { Colors } from '../../variables/color';

const AccountTable = () => {

    // 테스트 데이터
    const accountData = [
        {"name": "user1", "email": "email1@gmail.com", "password": "12345678"},
        {"name": "user2", "email": "email1@gmail.com", "password": "12345678"},
        {"name": "user3", "email": "email1@gmail.com", "password": "12345678"},
    ];


    const AccountComponent = accountData.map((a, idx) => {

        
        // 마우스 올려놓으면 색깔 변함
        const TableRawComponent = styled.tr`
            &:hover {
                background-color: #E6F3E3;
            }
        `
        
        // 테이블 레코드 렌더링
        return (
            <TableRawComponent key={idx}>
                <th style={{ 
                    display: "flex", flexWrap: "wrap", 
                    marginTop: "10px", marginBottom: "10px"}}>{a['name']}</th>
                <td>{a['email']}</td>
                <td>{a['password']}</td>
            </TableRawComponent>
        )
    })


    // 테이블 전체 렌더링
    return (
        <table style={{ 
                margin: "20px 0px 20px 0px", 
                width: "100%",
            }}>
            <thead style={{
                    borderBottom: "1px solid gray",
                }}>
                <th scope="col" style={{ paddingBottom: "10px" }}>Name</th>
                <th scope="col">Email</th>
                <th scope="col">Password</th>
            </thead>
            <tbody>
                {AccountComponent}
            </tbody>
        </table>
    )
}

const ConsoleControlComponent = () => {
    // 버튼들 모임

    return (
        <div style={{ dispaly: "flex", flexWrap: "wrap", paddingBttom: "30px" }}>
            <button className="custombutton-access" style={{ marginRight: "20px", marginBottom: "5px" }}>Add</button>
            <button className="custombutton-access-out" style={{ marginRight: "20px", marginBottom: "5px" }}>Modify</button>
            <button className="custombutton-danger-out" style={{ marginRight: "20px", marginBottom: "5px" }}>Delete</button>
        </div>);
}


const AccountSettingLayout = () => {

    const isPC = useMediaQuery(ResponsiveQuery.PC);
    const isTablet = useMediaQuery(ResponsiveQuery.TABLET);
    const isMobile = useMediaQuery(ResponsiveQuery.MOBILE);

    const paddingRightValue = () => {
        // 오른쪽 패딩
        if(isPC) return "200px";
        else if(isTablet) return "60px";
        else return "30px";
    }
    const paddingLeftValue = () => {
        // 왼쪽패딩
        if(isPC) return "80px";
        else if(isTablet) return "60px";
        else return "30px";
    }

    return (
        <Layout>
            
            <div>
                { isPC && 
                    <TitleLayoutPC>
                        <h1 style={{ color: Colors.COLORED_BOLD_COLOR, marginBottom: "30px" }}><strong>Accounts</strong></h1>
                    </TitleLayoutPC>
                }
                { isTablet &&
                    <TitleLayoutTablet>
                        <h1 style={{ color: Colors.COLORED_BOLD_COLOR, marginBottom: "30px"}}><strong>Accounts</strong></h1>
                    </TitleLayoutTablet>
                }
                { isMobile && 
                    <TitleLayoutMobile>
                        <h1 style={{ color: Colors.COLORED_BOLD_COLOR, marginBottom: "20px" }}><strong>Accounts</strong></h1>
                    </TitleLayoutMobile>
                }
                
            </div>

            <div style={{ width: "100%", height: "1px", background: "gray" }} />
            
            <div  style={{ paddingRight: `${paddingRightValue()}`, paddingLeft: `${paddingLeftValue()}`, paddingTop: "30px" }}>
                <ConsoleControlComponent />
                <AccountTable />
            </div>
        </Layout>
    )
}
export default AccountSettingLayout;
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
