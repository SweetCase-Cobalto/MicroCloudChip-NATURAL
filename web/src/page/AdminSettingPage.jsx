import MicrocloudchipNavbar from "../components/Navbar";
import styled from "styled-components";
import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';
import LeftMenuBar from "../components/LeftMenuBar";
import { Colors } from "../variables/color";
import { Image, Form, Row, Col } from "react-bootstrap";
import React from 'react';

import DefaultAccountIcon from '../asset/img/user-icon.svg';

const AccountSettingComponent = () => {

    const emailValue = "seokbong60@gmail.com";

    const storageSelectedItems = ["1KB", "5GB", "20GB", "500GB"];
    
    const StorageSelectedComponents = storageSelectedItems.map((item, idx) => 
        <option value={item} key={idx}>{item}</option>
    )

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
                    <Form.Label>Nickname</Form.Label>
                    <Form.Control type="text" placeholder="Only 6 Alphabets to 12 Alphabets" />
                </Form.Group>
                <Form.Group className="mb-3" controlId="formEmail">
                    <Form.Label>Email (Not Modified)</Form.Label>
                    <Form.Control type="email" placeholder="example@example.com" defaultValue={emailValue} disabled/>
                </Form.Group>
                
                <Row>
                    <Col md>
                        <Form.Group className="mb-3" controlId="formPassword">
                            <Form.Label>New Password</Form.Label>
                            <Form.Control type="text" placeholder="8 ~ 16" />
                        </Form.Group>
                    </Col>
                    <Col md>
                        <Form.Group className="mb-3" controlId="formPassword">
                            <Form.Label>Password Repeat</Form.Label>
                            <Form.Control type="text" placeholder="8 ~ 16" />
                        </Form.Group>
                    </Col>
                </Row>

                <Form.Label>Select Storage Type</Form.Label>
                <Form.Select aria-label="Default select example">
                    <option>Select Storage Type</option>
                    {StorageSelectedComponents}
                </Form.Select>

                <div style={{ display: "flex", marginTop: "20px" }}>
                    <button className="custombutton-access" style={{ marginRight: "10px" }}>Apply</button>
                    <button className="custombutton-unable">Cancel</button>
                </div>
            </Form>
            
        </div>
    )
}

const AdminLayout = () => {
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
                        <h1 style={ titleFontQuery  }><strong>Settings</strong></h1>
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
                    <AccountSettingComponent />
                </AccountSettingLayout>
            </div>

        </Layout>
    )
}

const AdminSettingPage = () => {
    // 관리자용 세팅 페이지

    const isPC = useMediaQuery(ResponsiveQuery.PC);

    return (
        <div>
            <MicrocloudchipNavbar />
            <div style={{ display: "flex" }}>
                {isPC && <LeftMenuBar />}
                <AdminLayout />
            </div>
        </div>
    )
}

export default AdminSettingPage;

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