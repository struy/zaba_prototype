import React, {useState, useEffect} from "react";

function Items() {
    // constructor(props) {
    //     super(props);
    //     this.state = {
    //         data: [],
    //         loaded: false,
    //         placeholder: "Loading"
    //     };
    // }
    const [data, setData] = useState([]);
    const [loaded, setLoaded] = useState(false);
    const [placeholder, setPlaceholder] = useState("Loading");


      useEffect(() => {
                fetch("items/")
            .then(response => {
                if (response.status > 400) {
                    setPlaceholder("Something went wrong!");
                }
                return response.json();
            })
            .then(data => {
                setData(data);
                setLoaded(true);
            });

      });

        return (
            <ul>
                {data.map(contact => {
                    return (
                        <li key={contact.id}>
                            {contact.title} - {contact.price}
                        </li>
                    );
                })}
            </ul>
        );

}

export default Items;

