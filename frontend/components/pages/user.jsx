import React from "react";

import Image from "../common/image.jsx";
import Page from "../common/page.jsx";
import PodcastGrid from "../podcasts/podcast-grid.jsx";
import FollowButton from "../auth/follow-button.jsx";

const User = React.createClass({
    render(){
        return (
            <Page>
                <div className="clearfix mxn2">
                    <div className="sm-col-12 p2">
                        <h1>{this.state.user.username}</h1>
                    </div>
                </div>
                <div className="clearfix mxn2">
                    <div className="sm-col sm-col-1 md-col-3 p2">
                        <Image src={this.state.user.avatar_url} className="full-width" />
                        <p><FollowButton user={this.state.user}/></p>
                    </div>
                    <div className="sm-col sm-col-11 md-col md-col-9 p2">
                        <h2>Subscriptions</h2>
                        <div className="clearfix mxn1">
                            {this.state.user.id ? (<PodcastGrid />) : "..."}
                        </div>
                    </div>
                </div>
            </Page>
        );
    },
    getInitialState(){
        return {user:{
            username: "Loading ...",
            avatar_url: "https://podato.herokuapp.com/img/logo.png"
        }};
    }
});

export default User;
