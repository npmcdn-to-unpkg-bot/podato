import Relay from "react-relay";

export const allQueries = {
    currentUser: () => Relay.QL`query { me }`,
    podcast: () => Relay.QL`query { podcast(id: $podcastId) }`,
    user: () => Relay.QL`query { user(id: $userId) }`
};

export function getQueries(names) {
    var result = {};
    names.forEach((key) => result[key] = allQueries[key])
    return result;
}