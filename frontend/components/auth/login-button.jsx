import React from "react";

const LoginButton = React.createClass({
    render(){
        var className = "button not-rounded " + (this.props.className || "");
        return (
            <a className={className} onClick={this.login} >Sign in with {this.props.authProvider}</a>
        )
    },
    login(e){
        e.preventDefault();
        //TODO log the user in.
    }
});

export default LoginButton;