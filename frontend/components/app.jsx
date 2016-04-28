import React from "react";
import Navbar from "./navbar/navbar.jsx";
import Playbar from "./playbar/playbar.jsx";

const App = React.createClass({
    render() {
        return (
            <div className="clearfix">
                <Navbar />
                <div className="container mt4">
                    {this.props.children}
                </div>
                <Playbar />
            </div>
        );
    }
});

export default App
