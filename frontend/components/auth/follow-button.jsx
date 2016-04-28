import React from "react"

import Spinner from "../common/spinner.jsx";

//TODO re-implement this to use GraphQL operations.
const FollowButton = React.createClass({
    componentWillMount(){
        window.WrongComponent = this;
        window.ListenerMixin = ListenerMixin;
        this.listenTo(CurrentUserStore, this.storeDidChange);
    },
    render(){
        if(!this.state.user) return (<span>Log in to subscribe.</span>);

        var className = "button " + (this.props.className || "");
        if(!this.state.isFollowing){
            return (
                <button {...this.props} className={className} onClick={this.follow} disabled={this.state.disabled}>Follow</button>
            )
        }
        className = "button bg-darken-4" + (this.props.className || "");
        return (
            <button {...this.props} className={className} onClick={this.unfollow} disabled={this.state.disabled}>Unfollow</button>
        )

    },
    makeState(){
        var state = {
            user: CurrentUserStore.getState().currentUser,
            isFollowing: CurrentUserStore.isFollowing(this.props.user.id)
        }
        return state
    },
    getInitialState(){
        return this.makeState();
    },
    follow(e){
        e.preventDefault();
        UserActions.follow(this.props.user.id);
        this.setState({disabled: true})
    },
    unfollow(e){
        e.preventDefault();
        UserActions.unfollow([this.props.user.id]);
        this.setState({disabled: true})
    },
    storeDidChange(){
        var newState = this.makeState();
        if(newState.isFollowing !== this.state.isFollowing){
            newState.disabled=false;
        }
        this.setState(newState);
    }
});

export default FollowButton;
