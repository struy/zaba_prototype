import React, {useState} from "react";
import {Nav, Navbar, NavItem, NavLink} from 'reactstrap';
import {
    NavLink as RRNavLink,
} from "react-router-dom";


function Header(props)  {

    return (
            <header id="header" className="fixed-top">
                <Navbar color="light" light expand="md">
                    <Nav>
                        <NavItem>
                            <NavLink to="/" activeClassName="active" tag={RRNavLink}>Home</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink to="/items" activeClassName="active" tag={RRNavLink}>Items</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink to="/map" activeClassName="active" tag={RRNavLink}>Map</NavLink>
                        </NavItem>
                    </Nav>
                </Navbar>
            </header>
    );
};

export default Header;