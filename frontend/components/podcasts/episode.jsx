import React from "react";
import {connect} from "react-redux";

import Image from "../common/image.jsx";

import {playEpisode, resume, pause} from "../../actions/playback-actions"

var Episode = React.createClass({
    render(){
        var published = new Date(this.props.episode.published);
        return (
            <div className="clearfix mxn1 py2 border-bottom border-silver">
                <div className="col col-2 px1">
                    <Image src={this.props.episode.image || this.props.podcast.image} className="full-width" />
                    {this.getPlayButton()}
                </div>
                <div className="col col-10 px1 lh1">
                    <span className="h5 bold">{this.props.episode.title}</span>
                    <span className="silver inline-block">
                        <i className="ml1 el el-calendar" aria-label="published:"/>
                        <date dateTime={published.toISOString()}>{published.toLocaleDateString()}</date> <i className="ml1 el el-time" aria-label="duration:" /> {this.props.episode.duration}</span><br/>
                    <span>{this.props.episode.subtitle}</span>
                </div>
            </div>
        )
    },
    makeState(){
        return {
            episodePlaying: playingEpisode && playingEpisode.guid == this.props.episode.guid,
            playing: PlaybackStore.getState().playing
        };
    },
    isEpisodePlaying(){
        return this.props.playback.episode.guid == this.props.episode.guid;
    },
    getPlayButton(){
        if(this.isEpisodePlaying() && this.props.playing){
            return <a onClick={this.pause}><i className="el el-pause"></i> pause</a>
        }else{
            return <a onClick={this.play}><i className="el el-play"></i> play</a>
        }
    },

    play(){
        if(this.isEpisodePlaying){
            resume();
        }else{
            playEpisode(this.props.episode);
        }
        return false;
    },

    pause(){
        pause();
        return false;
    }
});

export default connect((state) => {playback: state.get("playback").toObject()})(Episode);
