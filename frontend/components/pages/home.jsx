import React from "react";
import Relay from "react-relay";

import LoginButton from "../auth/login-button.jsx"
import PodcastGrid from "../podcasts/podcast-grid.jsx";
import ImportButton from "../podcasts/import-button.jsx";
import Page from "../common/page.jsx";

//todo rewrite this to use GraphQL
const Home = React.createClass({
    render(){
        var auth = this.getAuthButtons();
        var subscriptions = this.getSubscriptionsGrid();

        return (
            <Page>
                <h1 className="center">Podato</h1>
                <h2 className="center">Enjoy Podcasts Together</h2>
                <p className="center">
                    {auth}
                </p>
                <div className="clearfix">
                    {subscriptions}
                </div>
                <h3>Popular podcasts</h3>
                <div className="clearfix">
                    <PodcastGrid podcasts={this.state.popularPodcasts} className="sm-col sm-col-12" />
                </div>
                <hr />
            </Page>
        );
    },
    getAuthButtons(){
        var auth = [
            (<LoginButton authProvider="Facebook" className="m1" key="auth-1" />),
            (<LoginButton authProvider="Twitter" className="m1" key="auth-2" />),
            (<LoginButton authProvider="Google" className="m1" key="auth-3" />)
        ];

        if(this.state.authState === "progress") {
            auth = (<img src="/img/loading_bar.gif" />)
        }
        if(this.state.authState === "done") {
            auth = (<a>Get started</a>);
        }
        return auth
    },
    getSubscriptionsGrid(){
        if(this.state.authState === "done") {
            return [
                <h3 key="heading">Subscriptions</h3>,
                <ImportButton key="import" />,
                <PodcastGrid podcasts={this.state.userSubscriptions} className="sm-col sm-col-12" key="grid" />,
                <hr key="hr" />
            ]
        }
    },
    getInitialState(){
        return {authState: null, popularPodcasts: [], userSubscriptions: []};
    }
});

export default Relay.createContainer(Home, {
    fragments: {
        currentUser: () => Relay.QL`
        fragment on UserNode {
            username
        }
        `
    }
});
