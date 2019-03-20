/* eslint-disable */

import React from 'react';
import MotionElement from './MotionElement';
import axios from 'axios';
import qs from 'query-string';

class MotionList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            motions_list: [],
            loaded: false,
            endpoint: '/analytics/api/motions/',
            placeholder: 'Loading...',
        };
    }

    fetchData(params = null) {
        axios.get(this.state.endpoint, {
            params: { 'searchQuery': params },
            paramsSerializer: qs.stringify,
        }).then(data => this.setState({ motions_list: data.data, loaded: true }));
    }

    componentDidMount() {
        this.fetchData(null);
    }

    handleSearch(event) {
        let searchQuery = event.target.value.toLowerCase();
        this.fetchData(searchQuery);
    }

    render() {
        return (
            <React.Fragment>
                <div>
                    <input type="text" placeholder="Search..." className="search-field"
                           onChange={this.handleSearch.bind(this)} />
                    {!this.state.loaded ?
                        <p>{this.state.placeholder}</p> :
                        this.state.motions_list.map(function (el) {
                            return <MotionElement data={el} key={el.id} />;
                        })
                    }
                </div>
            </React.Fragment>);
    }
}

export default MotionList;
