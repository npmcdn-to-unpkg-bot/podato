import React from "react";
import Navbar from "./navbar/navbar.jsx";
import Playbar from "./playbar/playbar.jsx";

const App = React.createClass({
    render() {
        return (
            <div className="clearfix">
                <Navbar currentUser={this.props.currentUser} />
                <div className="container mt4">
                    {this.props.children}
                </div>
                <Playbar />
            </div>
        );
    }
});

export default Relay.createContainer(App, {
    fragments: {
        currentUser: () => Relay.QL`
            fragment on UserNode {
                ${Navbar.getFragment("currentUser")}
            }
        `
    }
});

