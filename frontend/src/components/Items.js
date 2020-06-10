import React, {Component} from "react";
import {render} from "react-dom";
import {Button, Spinner} from 'react-bootstrap';
import MainHeader from "./Layout/MainHeader";


class Items extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            loaded: false,
            placeholder: "Loading"
        };
    }

    componentDidMount() {
        fetch("items/api")
            .then(response => {
                if (response.status > 400) {
                    return this.setState(() => {
                        return {placeholder: "Something went wrong!"};
                    });
                }
                return response.json();
            })
            .then(data => {
                this.setState(() => {
                    return {
                        data,
                        loaded: true
                    };
                });
            });
    }

    render() {
        return (
            //Menu
            //Advertise
            //Breadcrumbs
            //Filter
            //list
            //Pagination
            //Footer
            //Add button
            <div>

                <MainHeader></MainHeader>

                <Breadcrumb>
                <Breadcrumb.Item href="#">Home</Breadcrumb.Item>
                <Breadcrumb.Item href="https://getbootstrap.com/docs/4.0/components/breadcrumb/">
                    Library
                </Breadcrumb.Item>
                <Breadcrumb.Item active>Data</Breadcrumb.Item>
                 </Breadcrumb>

                <main className="content">

                    <h1 className=" text-uppercase text-center my-4">Item list</h1>
                    <div className="row ">
                        <div className="col-md-6 col-sm-10 mx-auto p-0">
                            <div className="card p-3">
                                <ul className="list-group list-group-flush">
                                    {this.state.data.map(item => {
                                        return (
                                            <li style={{listStyleType: "none"}} key={item.id}>
                                                {item.id} - {item.title}
                                            </li>
                                        );
                                    })}
                                </ul>

                            </div>
                        </div>
                    </div>
                </main>
            </div>
        );
    }
}

export default Items;

