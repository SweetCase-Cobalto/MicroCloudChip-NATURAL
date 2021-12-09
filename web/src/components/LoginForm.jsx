import styled from 'styled-components';
import { Colors } from '../variables/color';
import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';

// Image Import
import LogoImg from '../asset/img/logo.svg';

const LoginForm = (props) => {
    // 로그인 폼

    const MobileForm = () => {
        // 모바일, 태블릿 에디션
        const isMobile = useMediaQuery(ResponsiveQuery.MOBILE);
        const isTablet = useMediaQuery(ResponsiveQuery.TABLET);
        return (
            (isMobile || isTablet) &&
            <div>
                <h1>Mobile</h1>
            </div>
        );
    }
    const PCForm = () => {
        // 데스크탑 에디션
        const isPC = useMediaQuery(ResponsiveQuery.PC);
        return (
            isPC &&
            <PCLayout>
                <center>
                    <img src={LogoImg} />
                    <h3>Microcloudchip LOGIN</h3>
                </center>
            </PCLayout>
        )
    }

    // 최종 렌더링
    return (
        <Layout>
            <MobileForm />
            <PCForm />
        </Layout>
    );
}

const Layout = styled.div`
    backgroundColor: white;
    border: 1px solid ${Colors.LOGIN_FORM_LINE};
`;

const PCLayout = styled.div`
    padding: 40px 30px 40px 30px;

`;
export default LoginForm;