import React from "react";
import moment from "moment";


import Page from "../common/page.jsx";
import Image from "../common/image.jsx";
import Spinner from "../common/spinner.jsx";
import SubscribeButton from "../podcasts/subscribe-button.jsx";
import Episode from "../podcasts/episode.jsx";


const Podcast = React.createClass({
    render(){
        var episodes = this.getEpisodes();
        var moreEpisodesButton = null;
        if (this.state.podcast && this.state.podcast.has_more_episodes && !this.state.fetchingEpisodes) {
            moreEpisodesButton = (
                <div className="clearfix py2">
                    <div className="col col-12 center">
                        <a className="blue button button-outline" onClick={this.fetchEpisodes}>more episodes</a>
                    </div>
                </div>
            )
        }
        if (this.state.fetchingEpisodes) {
            moreEpisodesButton = (
                <div className="clearfix py2">
                    <div className="col col-12 center">
                        <Spinner />
                    </div>
                </div>
            )
        }
        return (
            <Page>
                <div className="clearfix mxn2">
                    <div className="col col-3 p2 all-hide md-show">
                        <Image src={this.state.podcast.image} className="full-width"/>
                        <p><SubscribeButton podcast={this.state.podcast.id}/></p>
                        <p><strong>by:</strong> {this.state.podcast.author}</p>
                        <p><strong>subscribers:</strong> {this.state.podcast.subscribers}</p>
                        <p><strong>Updated:</strong> {moment(new Date(this.state.podcast.last_fetched)).fromNow()}</p>
                    </div>
                    <div className="col col-12 md-col-9 p2">
                        <h1 className="clearfix">{this.state.podcast.title}</h1>
                        <p className="md-hide"><SubscribeButton podcast={this.state.podcast.id}/></p>
                        <p className="md-hide"><strong>by:</strong> {this.state.podcast.author}</p>
                        <p className="clearfix"><Image src={this.state.podcast.image} className="left md-hide m1"
                                                       style={{width:"10%"}}/>{this.state.podcast.description}</p>
                        <hr />
                        {episodes}
                        {moreEpisodesButton}
                    </div>
                </div>
                <div className="clearfix mxn2">
                    <div className="col col-12 p2">
                        <p className="gray">{this.state.podcast.copyright}</p>
                    </div>
                </div>
            </Page>
        );
    },
    getEpisodes(){
        return this.state.podcast.episodes.map((e) => {
            return (<Episode episode={e} podcast={this.state.podcast} key={e.guid}/>);
        });
    },
    setPodcast(){
        var podcastId = this.props.params.splat;
        var podcast = PodcastsStore.getPodcast(decodeURIComponent(podcastId));

        if (!podcast) {
            PodcastsActions.fetchPodcast(podcastId);
        } else {
            this.setState({podcast: podcast});
        }
    }
});

export default tePodcast;
