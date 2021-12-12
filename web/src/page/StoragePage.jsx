import MicrocloudchipNavbar from "../components/Navbar";
import LeftMenuBar from "../components/LeftMenuBar";
import StorageLayout from "../components/storage/StorageLayout";
import {connect} from 'react-redux';

import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';
import React from 'react';

const StoragePage = (props) => {

    const isPC = useMediaQuery(ResponsiveQuery.PC);

    console.log(props);
    return (
        <div>
            <MicrocloudchipNavbar />
            <div style={{ display: "flex" }}>
                {isPC && <LeftMenuBar />}
                <StorageLayout />
            </div>
        </div>
    );
}

const mapStateToProps = (state) => (
    {loginStatus: state.TokenReducer }
)
// export default StoragePage;
export default connect(mapStateToProps)(StoragePage);