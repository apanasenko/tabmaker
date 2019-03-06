import React from 'react';
import axios from 'axios';
import qs from 'query-string';
import Loader from 'react-loader-spinner';
import DataGrid from './DataGrid';
import Graphics from './Graphics';
import { Redirect } from 'react-router-dom'

// https://www.chartjs.org/docs/

function posStats(arr) {
    const amount = arr.length;
    const winrate = arr.map(el => el[0]).reduce((a, b) => a + b, 0) / amount;
    const speaker = arr.map(el => el[1]).reduce((a, b) => a + b, 0) / amount;
    return { amount, winrate: winrate.toFixed(2), speaker: speaker.toFixed(2) };
}

class Profile extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            profile: {},
            loaded: false,
            endpoint: '/analytics/api/profile',
            placeholder: 'Loading...',
            to_login: false,
        };
    }

    async fetchProfile() {
        const response = await axios.get(this.state.endpoint, { paramsSerializer: qs.stringify });
        if (response.data.username) this.setState({ profile: response.data, loaded: true });
        else this.setState({ to_login: true, loaded: true })
    }

    componentDidMount() {
        this.fetchProfile();
    }


    render() {
        if (!this.state.loaded) return (
            <div className="loader">
                <Loader type="Triangle" color="#00BFFF" height="120" width="120" />
                <span>Collecting your data...</span>
            </div>
        );
        if(this.state.to_login) return (
          <Redirect to="/login" />
        );
        const statistics = (
            <React.Fragment>
                <DataGrid
                    overall={posStats(this.state.profile.analytics.overall).amount}
                    text="Всего игр сыграно"
                    og={posStats(this.state.profile.analytics.og).amount}
                    oo={posStats(this.state.profile.analytics.oo).amount}
                    cg={posStats(this.state.profile.analytics.cg).amount}
                    co={posStats(this.state.profile.analytics.co).amount}
                />
                <DataGrid
                    overall={posStats(this.state.profile.analytics.overall).winrate}
                    text="Среднее место"
                    og={posStats(this.state.profile.analytics.og).winrate}
                    oo={posStats(this.state.profile.analytics.oo).winrate}
                    cg={posStats(this.state.profile.analytics.cg).winrate}
                    co={posStats(this.state.profile.analytics.co).winrate}
                />
                <DataGrid
                    overall={posStats(this.state.profile.analytics.overall).speaker}
                    text="Средний спикерский"
                    og={posStats(this.state.profile.analytics.og).speaker}
                    oo={posStats(this.state.profile.analytics.oo).speaker}
                    cg={posStats(this.state.profile.analytics.cg).speaker}
                    co={posStats(this.state.profile.analytics.co).speaker}
                />
            </React.Fragment>
        );

        return (
            <div className="profile-wrapper">
                <div className="overall-statistics">
                    <div className="legend-wrapper">
                        <div className="header-name">
                            {this.state.profile.first_name} {this.state.profile.last_name}
                        </div>
                        <table cellSpacing="15">
                            <tbody>
                            <tr>
                                <td>ОП</td>
                                <td>ОО</td>
                            </tr>
                            <tr>
                                <td>ЗП</td>
                                <td>ЗО</td>
                            </tr>
                            </tbody>
                        </table>
                        <span>Всего игр отсужено: {this.state.profile.analytics.judgement}</span>
                    </div>
                    {statistics || ''}
                </div>
                <div className="chart-container">
                    <h2>Спикерские баллы по отборочным играм</h2>
                    <Graphics
                        labels={this.state.profile.analytics.overall.map(x => x[0])}
                        data={this.state.profile.analytics.overall.map(x => x[1])} />
                </div>
            </div>
        );
    }
}

export default Profile;

