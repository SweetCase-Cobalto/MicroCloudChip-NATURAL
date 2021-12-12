import { Navbar, Container, Nav, InputGroup, FormControl, Image, Tooltip, OverlayTrigger, Offcanvas } from "react-bootstrap";
import { Colors } from "../variables/color";

import NavbarLogImg from '../asset/img/navbar-logo.svg';
import DefaultUserLogoImg from '../asset/img/user-icon.svg'

import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';

import { useState } from "react";

import LeftMenuBar from './LeftMenuBar';
import React from 'react';

const MicrocloudchipNavbar = () => {
    // 네비바

    // 화면 너비 상태
    const isPC = useMediaQuery(ResponsiveQuery.PC);
    const isTablet = useMediaQuery(ResponsiveQuery.TABLET);

    const HelpTooltipAboutClickLogo = (props) => {
        // 로고 클릭하기 전에 갖다대면 설명함
        if(!isPC) {
            return <Tooltip id="logo-tooltip" {...props}>
                Click To See Menu!
            </Tooltip>
        } else {
            return <div></div>
        }
    }

    // 태블릿 모바일일 경우 로고버튼 누르면 메뉴가 나타나게 하는 컨트롤
    const [showMenu, setShowMenu] = useState(false);


    const showMenuHandler = () => {
        // PC에서는 작동하지 않는다
        if(!isPC) {
            setShowMenu(true);
        }
    }

    if(isPC && showMenu) {
        // PC판으로 바꼈는데 메뉴가 열려있으면 닫는다.
        setShowMenu(false);
    }
    const closeMenuHandler = () => setShowMenu(false);

    return (
        <Navbar variant="dark" style={{
            backgroundColor: Colors.NAVBAR_COLOR
        }}>
            <Container>
                <Navbar.Brand>
                    <OverlayTrigger
                        placement="bottom"
                        delay={{show: 250, hide: 200}}
                        overlay={HelpTooltipAboutClickLogo}
                    >
                        <img
                            src={NavbarLogImg}
                            height="30"
                            className="d-inline-block align-top"
                            alt="Logo Img"
                            style={{ marginRight: "10px", cursor: "pointer" }}
                            onClick={showMenuHandler}
                        />
                    </OverlayTrigger>
                    
                    {isPC && "MICROCLOUDCHIP"}
                    <Offcanvas show={showMenu} onHide={closeMenuHandler} style={{ width: "240px" }}>
                        <LeftMenuBar />    
                    </Offcanvas>
                </Navbar.Brand>

                {(isPC || isTablet) &&
                <Nav className="me-auto" style={{ display: "flex" }}>
                    <InputGroup className="form-inline my-2 my-lg-0">
                        <FormControl
                            placeholder="Search.."
                        />
                        <button className="custombutton-access-out" >
                          Search
                        </button>
                    </InputGroup>
                </Nav>}

                <Nav className="justify-content-end">
                    <Image
                        src={DefaultUserLogoImg}
                        height="30"
                        roundedCircle 
                    />
                </Nav>
            </Container>
        </Navbar>
    );
}
export default MicrocloudchipNavbar;