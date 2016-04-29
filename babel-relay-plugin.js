var request = require("sync-request");

var getBabelRelayPlugin = require("babel-relay-plugin");

var getGraphQLSchema = function() {
    var resp = request("POST", "http://localhost:9999/graphql/", {
        json: {
            query: require("graphql/utilities").introspectionQuery
        }
    });
    return JSON.parse(resp.getBody("utf8")).data;
};

module.exports = getBabelRelayPlugin(getGraphQLSchema());