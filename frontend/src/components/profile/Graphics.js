/* eslint-disable */

import React from 'react';
import { Line } from 'react-chartjs-2';

class Graphics extends React.Component {
    render() {
        const data = {
            labels: this.props.labels,
            datasets: [{
                label: '',
                borderWidth: 1,
                data: this.props.data,
                type: 'line',
                lineTension: 0.2,
                backgroundColor: 'rgba(75,192,192,0.4)',
                borderColor: 'rgba(75,192,192,1)',
                borderCapStyle: 'butt',
                borderJoinStyle: 'miter',
                pointBorderColor: 'rgba(75,192,192,1)',
                pointBorderWidth: 2,
                pointHoverRadius: 3,
                pointHoverBackgroundColor: 'rgba(75,192,192,1)',
                pointHoverBorderColor: 'rgba(220,220,220,1)',
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
            }],
        };
        return (
            <div className="graphic-wrapper">
                <Line data={data}
                      options={{
                          legend: {
                              display: false,
                          },
                          scales: {
                              xAxes: [{
                                  display: false,
                              }],
                          },
                          maintainAspectRatio: false,
                          responsive: true,
                      }}
                />
            </div>
        );
    }
}

export default Graphics;

