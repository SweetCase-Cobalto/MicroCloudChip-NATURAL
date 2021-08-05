import styled from "styled-components";
import "../asset/font/font.css";

const Footer = () => {
    return (
        <Layer>
            <p>MicroCloudChip NATURAL</p>
            <p>v0.0.1-Alpha1</p>
            <p>Copyright 2021. Sweetcase. All rights reserved</p>
        </Layer>
    );
}
const Layer = styled.div`
    padding-top: 30px;
    width: 100%;
    height: 160px;
    background-color: #137813;
    color: white;
    text-align: center;
    font-family: "Gothic A1";
    margin-top: 50px;
    font-size: 0.8em;
`
export default Footer;