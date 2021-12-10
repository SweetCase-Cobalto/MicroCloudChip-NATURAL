import MicrocloudchipNavbar from "../components/Navbar";
import LeftMenuBar from "../components/LeftMenuBar";

import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';

const StoragePage = () => {

    const isPC = useMediaQuery(ResponsiveQuery.PC);

    return (
        <div>
            <MicrocloudchipNavbar />
            <div style={{ display: "flexs" }}>
                {isPC && <LeftMenuBar />}
            </div>
        </div>
    );
}

export default StoragePage;