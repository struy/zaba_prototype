import React, {useState} from "react";
import {Nav, Navbar, NavItem, NavLink} from 'reactstrap';
import { NavLink as RRNavLink } from 'react-router-dom';


const Header = () => {

    return (
        <header id="header" className="fixed-top">
            <Navbar color="light" light expand="md">

                <Nav>
                    <NavItem>
<NavLink to="/home" activeClassName="active" tag={RRNavLink}>About</NavLink>                     </NavItem>
                    <NavItem>
                        <NavLink href="#">Link</NavLink>
                    </NavItem>
                    <NavItem>
                        <NavLink href="#">Another Link</NavLink>
                    </NavItem>
                    <NavItem>
                        <NavLink disabled href="#">Disabled Link</NavLink>
                    </NavItem>
                </Nav>
            </Navbar>

        </header>
    );
};

export {Header};