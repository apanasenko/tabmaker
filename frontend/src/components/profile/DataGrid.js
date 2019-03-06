import React from 'react';

class DataGrid extends React.Component {
    render() {
        return (
            <div className="statsContainer">
                <dl>
                    <dt>
                        {this.props.overall}
                    </dt>
                    <dd>{this.props.text}</dd>
                </dl>
                <div className="statsDetails">
                    <table cellSpacing="15">
                        <tbody>
                        <tr>
                            <td>{this.props.og}</td>
                            <td>{this.props.oo}</td>
                        </tr>
                        <tr>
                            <td>{this.props.cg}</td>
                            <td>{this.props.co}</td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }
}

export default DataGrid;

