import React from "react";
import Relay from "react-relay";
import {Link} from "react-router";

import SearchBox from "./search-box.jsx"

const Navbar = React.createClass({
    render(){
        var userInfo = "";
        if(this.props.currentUser){
            userInfo = <a className="col col-1"  className="button button-red">{this.props.currentUser.username}</a>
        }else{
            userInfo = <a className="col col-1" onClick={AuthActions.logout} className="button button-red">Log out</a>
        }
        return (
            <nav className="fixed top-0 left-0 right-0 bg-red white" style={{height:"2.5rem"}}>
                <div className="container">
                    <div className="clearfix" style={{height:"2.5rem"}}>
                        <Link to="/" className="col col-1" style={{height:"100%"}}><img src="/img/logo.png" style={{height:"100%"}}/></Link>
                        <Link to="/" className="button button-red col col-1">Home</Link>
                        <SearchBox className="col col-4" />
                        {userInfo}
                    </div>
                </div>
            </nav>
        )
    }
});

export default Relay.createContainer(Navbar, {
    fragments: {
        currentUser: () => Relay.QL`
            fragment on UserNode {
                username
            }
        `
    }
});
