import styled from "styled-components";
import "../asset/font/font.css";

const Footer = () => {
    return (
        <Layer>
            <p>MicroCloudChip NATURAL</p>
            <p>Copyright 2021. Sweetcase. All rights reserved</p>
        </Layer>
    );
}
const Layer = styled.div`
    padding-top: 30px;
    width: 100%;
    height: 120px;
    background-color: #137813;
    color: white;
    text-align: center;
    font-family: "Gothic A1";
    margin-top: 50px;
    font-size: 0.8em;
`
export default Footer;