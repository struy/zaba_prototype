import React, {Component} from "react";
import {useTranslation, Trans} from "react-i18next";
import {Link} from "react-router-dom";

export default function MainHeader() {
    const {t, i18n} = useTranslation();
    const changeLanguage = lng => {
        i18n.changeLanguage(lng);
    };

    return (

         // <nav>
         //      <ul>
         //        <li>
         //          <Link to="/">Home</Link>
         //        </li>
         //        <li>
         //          <Link to="/about">About</Link>
         //        </li>
         //        <li>
         //          <Link to="/users">Users</Link>
         //        </li>
         //      </ul>
         //    </nav>




        <header id="header" className="fixed-top">
            <div className="container">
                <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                     <Link  className="navbar-brand" to="/"><i className="fas fa-frog fa-2x"></i></Link>
                    <button className="navbar-toggler" type="button" data-toggle="collapse"
                            data-target="#navbarSupportedContent"
                            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav mr-auto">
                            <li className="nav-item active">
                                <a className="nav-link" href="{% url 'home' %}">   <Trans>  Home    </Trans> <span
                                    className="sr-only">(current)</span></a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link" href="#">   <Trans> Contacts </Trans></a>
                            </li>

                            <li className="nav-item">
                                <a className="nav-link" href="{% url 'items:map' %}">   <Trans> Map </Trans></a>
                            </li>

                            <li className="nav-item"><a className="nav-link" href="/admin"> Admin</a></li>
                            <li className="nav-item"><a className="nav-link" href="/rosetta">Rosetta</a></li>

                            <li className="nav-item">
                                <a className="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">
                                </a>
                            </li>

                            <li className="nav-item">
                                <a className="nav-link" href="logout">
                                    Logout
                                </a></li>
                            <li className="nav-item">
                                <a className="nav-link" href="login">Log-in</a>
                            </li>
                        </ul>

                              <button onClick={() => changeLanguage("de")}>de</button>
                              <button onClick={() => changeLanguage("en")}>en</button>

                    </div>
                </nav>

            </div>

        </header>


    );
}
