import React, {Component} from "react";
import {render} from "react-dom";
import SideBar from "./SideBar";
import {Header} from "./Header";
import {Footer} from "./Footer";
import Items from "./Items";


class App extends Component {


    render() {
        return (
            <>
                <SideBar></SideBar>
                <Header></Header>
                <Items></Items>
                <Footer></Footer>
            </>
        );
    }
}

export default App;

const container = document.getElementById("app");
render(<App/>, container);