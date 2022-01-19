import MicrocloudchipNavbar from "../components/Navbar";
import styled from "styled-components";
import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';
import LeftMenuBar from "../components/LeftMenuBar";
import { Colors } from "../variables/color";
import { Image, Form, Row, Col } from "react-bootstrap";
import React from 'react';

import DefaultAccountIcon from '../asset/img/user-icon.svg';
import { connect } from "react-redux";

const AccountSettingComponent = (props) => {

    const storageSelectedItems = ["1KB", "5GB", "20GB", "500GB"];
    const StorageSelectedComponents = storageSelectedItems.map((item, idx) => 
        <option value={item} key={idx}>{item}</option>
    )

    const onSubmitHandler = (e) => {
        console.log(e.target);
    }
    const userInfo = props.userInfo;

    return (
        <div style={{
            width: "100%",
            display: "flex",
            paddingTop: "40px"
        }}>
            <Image 
                src={DefaultAccountIcon} alt="icon" 
                width="150px" height="150px"
                style={{ marginRight: "30px" }}
                roundedCircle />
            
            <Form style={{ width: "100%" }}>
                <Form.Group className="mb-3" controlId="formNickName">
                    <Form.Label>Nickname (Not Modified)</Form.Label>
                    <Form.Control type="text" placeholder="Only 4 Alphabets to 16 Alphabets" defaultValue={userInfo.name} disabled />
                </Form.Group>
                <Form.Group className="mb-3" controlId="formEmail">
                    <Form.Label>Email (Not Modified)</Form.Label>
                    <Form.Control type="email" placeholder="example@example.com" defaultValue={userInfo.email} disabled/>
                </Form.Group>
                
                <Row>
                    <Col md>
                        <Form.Group className="mb-3" controlId="formPassword">
                            <Form.Label>New Password</Form.Label>
                            <Form.Control type="text" placeholder="8 ~ 128 length" />
                        </Form.Group>
                    </Col>
                    <Col md>
                        <Form.Group className="mb-3" controlId="formPassword">
                            <Form.Label>Repeat New Password</Form.Label>
                            <Form.Control type="text" placeholder="8 ~ 128 length" />
                        </Form.Group>
                    </Col>
                </Row>
            
                <div style={{ display: "flex", marginTop: "20px" }}>
                    <button className="custombutton-access" style={{ marginRight: "10px" }}>Apply</button>
                </div>
            </Form>
            
        </div>
    )
}

/* TODO 용량 사이즈 수정하는 폼 (아직 용량 수정에 대한 서버 대응 기능을 구현하지 않아 보류)
    <Form.Label>Select Storage Type</Form.Label>
    <Form.Select aria-label="Default select example">
        <option>Select Storage Type</option>
        {StorageSelectedComponents}
    </Form.Select>
*/

const AdminLayout = (props) => {
    // 관리자 레이아웃

    const isPC = useMediaQuery(ResponsiveQuery.PC);
    const isTablet = useMediaQuery(ResponsiveQuery.TABLET);
    const isMobile = useMediaQuery(ResponsiveQuery.MOBILE);

    // CSS Query
    const titleFontQuery = { color: Colors.COLORED_BOLD_COLOR, marginBottom: "30px"};
    const paddingQuery = () => {
        if(isPC) return "0px 200px 100px 80px";
        else if(isTablet) return "0px 60px 100px 60px";
        else return "0px 30px 100px 30px";
    }

    return (
        <Layout>

            <div>
                { isPC && 
                    <TitleLayoutPC>
                        <h1 style={ titleFontQuery }><strong>Settings</strong></h1>
                    </TitleLayoutPC>
                }
                { isTablet &&
                    <TitleLayoutTablet>
                        <h1 style={ titleFontQuery }><strong>Settings</strong></h1>
                    </TitleLayoutTablet>
                }
                { isMobile && 
                    <TitleLayoutMobile>
                        <h1 style={ titleFontQuery }><strong>Settings</strong></h1>
                    </TitleLayoutMobile>
                }
                <div style={{ width: "100%", height: "1px", background: "gray" }} />
            
                <AccountSettingLayout style={{ padding: `${paddingQuery()}` }}>
                    <h2 style={titleFontQuery}><strong>Account Setting</strong></h2>
                    <AccountSettingComponent userInfo={props.userInfo} />
                </AccountSettingLayout>
            </div>

        </Layout>
    )
}

const AdminSettingPage = (props) => {
    // 관리자용 세팅 페이지
    const isPC = useMediaQuery(ResponsiveQuery.PC);

    return (
        <div>
            <MicrocloudchipNavbar />
            <div style={{ display: "flex" }}>
                {isPC && <LeftMenuBar />}
                <AdminLayout userInfo={props.loginStatus} />
            </div>
        </div>
    )
}
const mapStateToProps = (state) => (
    {loginStatus: state.UserInfoReducer }
)
export default connect(mapStateToProps)(AdminSettingPage);

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
const AccountSettingLayout = styled.div`
    margin-top: 40px;
`