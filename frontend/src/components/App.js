import React, {Component} from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";
import Items from "./Items";
import MainHeader from "./Layout/MainHeader";


export default function App() {
    return (
        <Router>
          <div>
              <MainHeader> </MainHeader>
            <Switch>
              <Route path="/about">
                <span> about</span>
              </Route>
              <Route path="/users">
               <span>users</span>
              </Route>
              <Route path="/">
                <Items />
              </Route>
            </Switch>
          </div>
        </Router>

      );

}



