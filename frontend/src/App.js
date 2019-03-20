/* eslint-disable */

import React, { Component } from "react";
import { Route, HashRouter } from "react-router-dom";
import Profile from "./components/profile/Profile";
import MotionList from "./components/motion/MotionList";
import './App.css';

class Main extends Component {
    render() {
        return (
            <HashRouter>
                <div className="router-container">
                    {/*<h1>Simple SPA</h1>*/}
                    {/*<ul className="header">*/}
                        {/*<li><NavLink exact to="/">Home</NavLink></li>*/}
                        {/*<li><NavLink to="/motions">Stuff</NavLink></li>*/}
                    {/*</ul>*/}
                    <a className="header__logo" href="/"><span>Tabmaker</span></a>
                    <div className="content">
                        <Route exact path="/profile" component={ Profile } />
                        <Route path="/motions" component={ MotionList } />
                    </div>
                </div>
            </HashRouter>
        );
    }
}

export default Main;
