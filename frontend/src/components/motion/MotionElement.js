import React from 'react';

class MotionElement extends React.Component {
    render() {
        return (
            <li className="motion_element">
                <div className="motion-info">
                    <div className="motion-motion"> {this.props.data.motion} </div>
                    <div className="motion-infoslide"> {this.props.data.infoslide} </div>
                    <div className="motion-governmentscore">
                        Правительство:
                        {(this.props.data.analysis) ? this.props.data.analysis.government_score : ' unknown'}
                    </div>
                    <div className="motion-oppositionscore">
                        Оппозиция:
                        {(this.props.data.analysis) ?
                            this.props.data.analysis.opposition_score : ' unknown'}
                    </div>
                    <hr />
                </div>
            </li>
        );
    }
}

export default MotionElement;
