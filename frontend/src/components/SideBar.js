import React, { Component } from "react";
import {Col, Container, Row} from "reactstrap";

class SideBar extends Component {


  render() {
    return (
        <Container>
          <Row>
              <Col sm="4">.col-sm-4</Col>
          </Row>
        </Container>
    );
  }
}

export default SideBar;

