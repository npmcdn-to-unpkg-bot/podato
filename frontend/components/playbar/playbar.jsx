import React from "react";
import {connect} from "react-redux";

import utils from "../../utils";

import Image from "../common/image.jsx";
import ProgressBar from "./progress-bar.jsx";

import {play, pause} from "../../actions/playback-actions";



const PlayBar = React.createClass({
    render(){
        if(!this.props.episode){
            return null;
        }
        var playButton = <button className="button button-red col col-1" onClick={play} style={{height:"2.5rem"}}><i className="el el-play" /></button>;
        if(this.props.playing){
            playButton = <button className="button button-red col col-1" onClick={pause} style={{height:"2.5rem"}}><i className="el el-pause"/></button>
        }
        return (
            <nav className="fixed bottom-0 left-0 right-0 bg-red white px4" style={{height:"2.5rem"}}>
                <ProgressBar progress={this.props.position / this.props.duration} duration={this.props.duration}/>
                <div className="container">
                    <div className="clearfix" style={{height:"2.5rem"}}>
                        <div className="col col-1"><Image src={this.props.episode.image} style={{height: "2.5rem"}} /></div>
                        <button className="button button-red col col-1" style={{height:"2.5rem"}}><i className="el el-backward" /></button>
                        {playButton}
                        <button className="button button-red col col-1" style={{height:"2.5rem"}}><i className="el el-forward" /></button>
                        <div className="col col-3" style={{height:"2.5rem", "lineHeight":"2.5rem"}}>{utils.formatTime(this.props.position)} / {utils.formatTime(this.state.duration)}</div>
                    </div>
                </div>
            </nav>
        )
    }
});

export default connect((state) => state.get("playback").toObject())(Playbar);
