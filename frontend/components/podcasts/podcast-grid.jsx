import React from "react";
import PodcastTile from "./podcast-tile.jsx";
import  Spinner from "../common/spinner.jsx";

const PodcastGrid = React.createClass({
    render(){
        if(this.props.podcasts == void(0)){
            return <Spinner />
        }
        return (<div {...this.props}>
                    <div className="clearfix mxn2">
                        {this.props.podcasts.map((podcast) => {
                            return <PodcastTile podcast={podcast} key={podcast.id} />
                        })}
                    </div>
                </div>)
    }
});

export default PodcastGrid;
