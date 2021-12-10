import { Navbar, Container, Nav, Button, InputGroup, FormControl, Image } from "react-bootstrap";
import { Colors } from "../variables/color";

// img import
import NavbarLogImg from '../asset/img/navbar-logo.svg';
import DefaultUserLogoImg from '../asset/img/user-icon.svg'

import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';

const MicrocloudchipNavbar = () => {
    // 네비바
    const isPC = useMediaQuery(ResponsiveQuery.PC);
    const isTablet = useMediaQuery(ResponsiveQuery.TABLET);

    return (
        <Navbar variant="dark" style={{
            backgroundColor: Colors.NAVBAR_COLOR
        }}>
            <Container>
                <Navbar.Brand>
                    <img
                        src={NavbarLogImg}
                        height="30"
                        className="d-inline-block align-top"
                        alt="Logo Img"
                        style={{ marginRight: "10px" }}
                    />
                    {isPC && "MICROCLOUDCHIP"}
                </Navbar.Brand>

                {(isPC || isTablet) &&
                <Nav className="me-auto" style={{ display: "flex" }}>
                    <InputGroup className="form-inline my-2 my-lg-0">
                        <FormControl
                            placeholder="Search.."
                        />
                        <Button className="custombutton-access-out" >
                          Search
                        </Button>
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