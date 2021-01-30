import React, {Component} from "react";
import {render} from "react-dom";
import {
    NavLink as RRNavLink,
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    useRouteMatch,
    useParams
} from "react-router-dom";
import Items from "./Items";
import {Footer} from "./Footer";
import Header from "./Header";
import Home from "./Home";
import Map from "./Map";


class App extends Component {


    render() {
        return (
            <Router>
                <div>
                    <Header/>
                    <hr/>
                    <Switch>
                        <Route path="/">
                            <Home/>
                        </Route>
                        <Route path="/items">
                            <Items/>
                        </Route>
                        <Route path="/map">
                            <Map/>
                        </Route>
                    </Switch>
                    <Footer/>
                </div>
            </Router>
        );
    }
}

export default App;

const container = document.getElementById("app");
render(<App/>, container);