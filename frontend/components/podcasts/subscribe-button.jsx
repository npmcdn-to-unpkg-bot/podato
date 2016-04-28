import React from "react";

import Spinner from "../common/spinner.jsx";

const SubscribeButton = React.createClass({
    render(){
        if(!this.props.user) return (<span>Log in to subscribe.</span>);
        if(!this.props.isSubscribed){
            if(this.props.fetching){
                return (<Spinner />);
            }
            return (<span>Something went wrong while trying to fetch your subscriptions.</span>);
        }

        var className = "button " + (this.props.className || "");
        if(!this.props.isSubscribed){
            return (
                <button {...this.props} className={className} onClick={this.subscribe} disabled={this.state.disabled}>Subscribe</button>
            )
        }
        className = "button bg-darken-4" + (this.props.className || "");
        return (
            <button {...this.props} className={className} onClick={this.unsubscribe} disabled={this.state.disabled}>Unsubscribe</button>
        )
    },
    getInitialState(){
        return {
            disabled: false
        }
    },
    subscribe(e){
        e.preventDefault();
        this.setState({disabled: true});
    },
    unsubscribe(e){
        e.preventDefault();
        this.setState({disabled: true});
    }
});

export default SubscribeButton;
