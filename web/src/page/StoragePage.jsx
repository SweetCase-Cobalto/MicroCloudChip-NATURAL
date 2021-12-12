import MicrocloudchipNavbar from "../components/Navbar";
import LeftMenuBar from "../components/LeftMenuBar";
import StorageLayout from "../components/storage/StorageLayout";

import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';
import React from 'react';

const StoragePage = () => {

    const isPC = useMediaQuery(ResponsiveQuery.PC);

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

export default StoragePage;